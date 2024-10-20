from datetime import datetime
import os
import string
from moviepy.editor import VideoFileClip
import shutil
from PIL import Image
from openapi_server.domain.repositories.file_repository import FileRepository, InMemoryFileRepository
from pathlib import Path
from typing import IO
from typing import List
from openapi_server.domain.models.file import File
from openapi_server.domain.models.transcription import Segment
import uuid
from werkzeug.utils import secure_filename
import boto3
from abc import ABC, abstractmethod
from botocore.exceptions import ClientError
import tempfile
from remotion_lambda import RenderMediaParams
from remotion_lambda import RemotionClient
import io


class InvalidFileException(Exception):
    pass


class FileStoreException(Exception):
    pass


class FileRenderException(Exception):
    pass


class FileStore(ABC):
    @abstractmethod
    def store(self, filename: str, content: IO[bytes]):
        pass

    @abstractmethod
    def get_url(self, filename: str):
        pass


class AWSFileStore(FileStore):
    def __init__(
            self,
            access_key="",
            secret_key="",
            region="us-east-1",
            bucket_name="music-ai-sub-upload-bucket",
            prefix="uploads/"):
        if not access_key or not secret_key:
            access_key = os.getenv("AWS_ACCESS_KEY_ID")
            secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.s3 = boto3.client("s3",
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key,
                               region_name=region
                               )
        self.prefix = prefix if prefix[-1] == "/" else f"{prefix}/"
        self.bucket_name = bucket_name

    def store(self, filename: str, content: IO[bytes]):
        try:
            self.s3.upload_fileobj(
                content, self.bucket_name, f"{self.prefix}{filename}")
        except ClientError as e:
            raise FileStoreException(f"boto client error: {e}")
        except Exception as e:
            raise FileStoreException(f"unexpected error: {e}")

    def get_url(self, filename: str) -> string:
        return f"https://{self.bucket_name}.s3.amazonaws.com/{self.prefix}{filename}"

    def delete(self, filename: str) -> None:
        self.s3.delete_object(self.bucket_name, f"{self.prefix}{filename}")

    def delete_all(self) -> None:
        res = self.s3.list_objects_v2(self.bucket_name, self.prefix)
        for object in res['Contents']:
            self.s3.delete_object(self.bucket_name, object['Key'])


class LocalFileStore(FileStore):
    def __init__(self, file_root_dir: Path = "/tmp/mais/file"):
        self.file_root_dir = file_root_dir
        os.makedirs(self.file_root_dir, exist_ok=True)

    def _get_file_dir_path(self, filename: Path) -> Path:
        return self.file_root_dir / Path(filename.stem)

    def _get_file_path(self, filename: Path) -> Path:
        return self._get_file_dir_path(filename) / filename

    def store(self, filename: string, content: IO[bytes]) -> string:
        # sanitize filename for secure fs storage
        filename = Path(secure_filename(filename))
        if not filename:
            raise FileStoreException(f"invalid filename: {filename}")

        os.makedirs(self._get_file_dir_path(filename), exist_ok=True)

        file_path = self._get_file_path(filename)

        # write file in chunks
        chunk_size = 1024 * 1024
        with open(file_path, 'wb') as file:
            while True:
                chunk = content.read(chunk_size)
                if not chunk:
                    break
            file.write(chunk)

        return file_path

    def delete(self, filename: string) -> None:
        dir_path = self._get_file_dir_path(Path(filename))
        if dir_path.exists():
            shutil.rmtree(dir_path)

    def delete_all(self) -> None:
        for f in os.listdir(self.file_root_dir):
            shutil.rmtree(self.file_root_dir / Path(f))

    def get_url(self, filename: string) -> str:
        return f'/videos/{Path(filename).stem}/{filename}'


class FileService:
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    audio_extensions = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma']

    def __init__(self, repository: FileRepository = None,
                 file_store: FileStore = None):
        if not repository:
            repository = InMemoryFileRepository()

        self.repository = repository

        if not file_store:
            file_store = LocalFileStore()
        self.file_store = file_store

    @staticmethod
    def _extract_image(file_path, time=1) -> IO[bytes]:
        clip = VideoFileClip(file_path)
        frame = clip.get_frame(time)
        image = Image.fromarray(frame)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        return image_bytes

    @staticmethod
    def _is_video_file(file_path: Path) -> bool:
        try:
            clip = VideoFileClip(file_path)
            clip.close()
        except Exception:
            return False

        return True

    def delete(self, filename: str):
        self.file_store.delete(filename)
        self.repository.delete(filename)

    def delete_all(self):
        self.file_store.delete_all()
        self.repository.delete_all()

    def is_valid(self, filename: Path):
        if filename.suffix in FileService.video_extensions or filename.suffix in FileService.audio_extensions:
            return True
        return False

    def get_preview_image(self, content: IO[bytes]) -> IO[bytes]:
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(content.read())
            temp_file_path = temp_file.name
            if self._is_video_file(temp_file_path):
                try:
                    preview_image = self._extract_image(temp_file_path)
                    return preview_image
                except Exception as e:
                    print(e)

    def add(self, filename: Path, content: IO[bytes]):
        if not self.is_valid(filename):
            raise InvalidFileException

        id = str(uuid.uuid4())
        content.seek(0)
        preview_image = self.get_preview_image(content)
        if preview_image:
            image_filename = Path(filename.stem + ".jpg")
            preview_image.seek(0)
            self.file_store.store(image_filename, preview_image)

        # store file
        content.seek(0)
        self.file_store.store(filename, content)

        # store file metadata
        f_metadata = {
            "filename": str(filename),
            "video_url": self.file_store.get_url(filename),
            "image_url": self.file_store.get_url(image_filename) if preview_image else "",
            "upload_date": datetime.now(),
            "id": id,
        }
        self.repository.add(File(**f_metadata))

    def get(self, filename: str):
        return self.repository.get_by_id(filename)

    def get_all(self) -> List[File]:
        return self.repository.get_all()


class RemotionFileRender:
    def __init__(
            self,
            function_name: str = "",
            serve_url: str = "",
            region: str = "us-east-1",
            access_key: str = "",
            secret_key: str = "",
            composition="MusicAISubComposition"):
        if not function_name:
            function_name = os.getenv("REMOTION_APP_FUNCTION_NAME")

        if not serve_url:
            serve_url = os.getenv("REMOTION_APP_SERVE_URL")

        if not access_key or not secret_key:
            access_key = os.getenv("AWS_ACCESS_KEY_ID")
            secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        self.client = RemotionClient(region=region,
                                     serve_url=serve_url,
                                     function_name=function_name,
                                     access_key=access_key,
                                     secret_key=secret_key)
        self.region = region
        self.composition = composition

    def render(self, video_url: str = "",
               segments: List[Segment] = [], fps: int = 30) -> IO[bytes]:
        # Set render request
        render_params = RenderMediaParams(
            composition=self.composition,
            input_props={
                "segments": [segment.model_dump() for segment in segments],
                "src": video_url,
                "fps": fps,
            },
            region=self.region,
            codec="h264",
        )
        render_response = self.client.render_media_on_lambda(render_params)
        if render_response:
            # Execute render request
            print("Render ID:", render_response.render_id)
            print("Bucket name:", render_response.bucket_name)
            # Execute progress request
            progress_response = self.client.get_render_progress(
                render_id=render_response.render_id, bucket_name=render_response.bucket_name)
            while progress_response and not progress_response.done:
                print("Overall progress")
                print(str(progress_response.overallProgress * 100) + "%")
                progress_response = self.client.get_render_progress(
                    render_id=render_response.render_id, bucket_name=render_response.bucket_name)
            return self._download(
                render_response.bucket_name, progress_response.outKey)

    def _download(self, bucket_name: str, key: str) -> IO[bytes]:
        s3 = boto3.client('s3')
        file_obj = io.BytesIO()
        s3.download_fileobj(bucket_name, key, file_obj)
        return file_obj
