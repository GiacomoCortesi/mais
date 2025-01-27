from datetime import datetime
import logging
import os
from moviepy import VideoFileClip
from PIL import Image
from api.repositories.file import FileRepository, FileStore, InMemoryFileRepository, LocalFileStore
from pathlib import Path
from typing import IO, Optional
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
    
    @staticmethod
    def get_video_size(file_path: Path) -> dict:
        # Load the video file
        video = VideoFileClip(file_path)
        
        # Get dimensions
        width, height = video.size
        
        # Close the video to release resources
        video.close()

        return width, height

    @staticmethod
    def get_video_duration(file_path: Path) -> float:
        # Load the video file
        video = VideoFileClip(file_path)
        
        # Get duration (in seconds)
        duration = video.duration
        
        # Close the video to release resources
        video.close()
        
        return duration
    
    def get_video_info(self, content: IO[bytes]):
        video_info = {}
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(content.read())
            temp_file_path = temp_file.name
            if not self._is_video_file(temp_file_path):
                return None
            try:
                preview_image = self._extract_image(temp_file_path)
                video_info["preview_image"] = preview_image
            except Exception as e:
                self.logger.warning(f"Failed to extract image from file {temp_file_path}: {e}")
            try:
                duration = self.get_video_duration(temp_file_path)
                video_info["duration"] = duration
            except Exception as e:
                self.logger.warning(f"Failed to extract video duration from file {temp_file_path}: {e}")
            try:
                width, height = self.get_video_size(temp_file_path)
                video_info["width"] = width
                video_info["height"] = height
            except Exception as e:
                self.logger.warning(f"Failed to extract video dimensions from file {temp_file_path}: {e}")
        return video_info

    @staticmethod
    def get_video_dimensions_from_bytes(file_path: Path) -> Optional[dict]:
        try:
            clip = VideoFileClip(file_path)
            width, height = clip.size
            return {"width": width, "height": height}
        except Exception as e:
            print(f"Error getting video dimensions: {e}")
            return None

    def add(self, filename: Path | str, content: IO[bytes]) -> FileResponse:
        filename = Path(filename)
        
        if not self.is_valid(filename):
            raise InvalidFileException(filename)

        id = str(uuid.uuid4())
        content.seek(0)
        video_info = self.get_video_info(content)
        preview_image = video_info.get("preview_image", None)
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
            "width": video_info.get("width", None),
            "height": video_info.get("height", None),
            "duration": video_info.get("duration", None),
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
               segments: List[Segment] = [], fps: int = 30, width=None, height=None, duration=None, subtitle_config=None) -> IO[bytes]:
        render_params = RenderMediaParams(
            composition=self.composition,
            max_retries=3,
            
            input_props={
                "segments": [segment.model_dump() for segment in segments],
                "src": video_url,
                "fps": fps,
                "width": width,
                "height": height,
                "duration": duration,
                "subtitleConfig": subtitle_config.model_dump(),
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
                if len(progress_response.errors) > 0:
                    self.logger.error(f"rendering failed: {progress_response.errors}")
                    raise Exception(f"rendering failed: {progress_response.errors}")
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