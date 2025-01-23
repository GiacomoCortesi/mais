from datetime import datetime
import logging
import os
from moviepy import VideoFileClip
from PIL import Image
from api.repositories.file import FileRepository, FileStore, InMemoryFileRepository, LocalFileStore
from pathlib import Path
from typing import IO
from typing import List
from api.models import FileResponse
from api.models import Segment
import uuid
import boto3
import tempfile
from remotion_lambda import RenderMediaParams
from remotion_lambda import RemotionClient
import io

class FileServiceException(Exception):
    pass


class InvalidFileException(FileServiceException):
    def __init__(self, filename: str):
        self.message = f"File {filename} extension not supported"
        super().__init__(self.message)

class FileService:
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    audio_extensions = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma']

    def __init__(self, repository: FileRepository = None,
                 file_store: FileStore = None):
        self.logger = logging.getLogger(__name__)
        
        if not repository:
            self.logger.debug("using default in memory file repository")
            repository = InMemoryFileRepository()
        self.repository = repository

        if not file_store:
            self.logger.debug("using default local file store")
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
                    self.logger.warning(f"Failed to extract image from file {temp_file_path}: {e}")

    def add(self, filename: Path | str, content: IO[bytes]) -> FileResponse:
        filename = Path(filename)
        
        if not self.is_valid(filename):
            raise InvalidFileException(filename)

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
        f_metadata = FileResponse(**{
            "filename": str(filename),
            "video_url": self.file_store.get_url(filename),
            "image_url": self.file_store.get_url(image_filename) if preview_image else "",
            "upload_date": datetime.now(),
            "id": id,
        })
        self.repository.add(f_metadata)
        return f_metadata

    def get(self, filename: str):
        return self.repository.get_by_id(filename)
    
    def get_file(self, filename: str) -> IO[bytes]:
        return self.file_store.get_file(filename)

    def get_all(self) -> List[FileResponse]:
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

        self.logger = logging.getLogger(__name__)

    def render(self, video_url: str = "",
               segments: List[Segment] = [], fps: int = 30) -> IO[bytes]:
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
            self.logger.info(f"render id: {render_response.render_id}, bucket: {render_response.bucket_name}")
            progress_response = self.client.get_render_progress(
                render_id=render_response.render_id, bucket_name=render_response.bucket_name)
            while progress_response and not progress_response.done:
                self.logger.info(f"rendering progress: {progress_response.overallProgress * 100}%")
                progress_response = self.client.get_render_progress(
                    render_id=render_response.render_id, bucket_name=render_response.bucket_name)
            return self._download(
                render_response.bucket_name, progress_response.outKey)

    def _download(self, bucket_name: str, key: str) -> IO[bytes]:
        s3 = boto3.client('s3')
        file_obj = io.BytesIO()
        s3.download_fileobj(bucket_name, key, file_obj)
        file_obj.seek(0)
        return file_obj