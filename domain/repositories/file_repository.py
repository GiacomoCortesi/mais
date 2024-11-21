from abc import ABC, abstractmethod
from io import BytesIO
import logging
import os
from pathlib import Path
import shutil
from typing import IO, List

import boto3
from repositories.base_repository import BaseRepository
from models.file import File
from models.id import ID
import uuid
from typing import Dict
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError, BotoCoreError

class FileException(Exception):
    pass


class FileNotFoundException(FileException):
    def __init__(self, file_id: ID):
        self.message = f"File with ID {file_id} not found"
        super().__init__(self.message)



class FileStoreException(Exception):
    pass


class FileRepository(BaseRepository[File]):
    pass


class InMemoryFileRepository(FileRepository):
    def __init__(self):
        self.files: Dict[ID, File] = {}

    def get_all(self) -> List[File]:
        return list(self.files.values())

    def get_by_id(self, id: ID) -> File:
        f = self.files.get(id, None)
        if not f:
            raise FileNotFoundException(id)
        return f    

    def add(self, f: File) -> None:
        if not f.id:
            f.id = str(uuid.uuid4())
        self.files[f.filename] = f

    def delete(self, id: ID) -> None:
        self.files.pop(id, None)

    def delete_all(self) -> None:
        self.files = {}

    def update(self, f: File) -> None:
        self.files[f.filename] = f

class FileStore(ABC):
    @abstractmethod
    def store(self, filename: str, content: IO[bytes]):
        pass

    @abstractmethod
    def get_url(self, filename: str):
        pass

    @abstractmethod
    def get_file(self, filename: str) -> IO[bytes]:
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

        self.logger = logging.getLogger(__name__)

    def _run_s3(self, operation, *args, **kwargs):
        try:
            res = getattr(self.s3, operation)(*args, **kwargs)
            return res
        except ClientError as e:
            self.logger.error(f"boto client error: {e}")
            raise FileStoreException(f"boto client error: check aws credentials")
        except BotoCoreError as e:
            self.logger.error(f"boto core error: {e}")
            raise FileStoreException(f"boto core error: check network connectivity")
        except Exception as e:
            self.logger.error(f"unexpected error: {e}")
            raise FileStoreException(f"unexpected error: {e}")
    
    def store(self, filename: str, content: IO[bytes]):
        self._run_s3('upload_fileobj', content, self.bucket_name, f"{self.prefix}{filename}")

    def get_url(self, filename: str) -> str:
        return f"https://{self.bucket_name}.s3.amazonaws.com/{self.prefix}{filename}"

    def delete(self, filename: str) -> None:
        self._run_s3('delete_object', self.bucket_name, f"{self.prefix}{filename}")

    def delete_all(self) -> None:
        res = self._run_s3('list_objects_v2', self.bucket_name, self.prefix)
        for object in res['Contents']:
            res = self._run_s3('delete_object', self.bucket_name, object['Key'])

    def get_file(self, filename: str) -> IO[bytes]:
        res = self._run_s3('get_object', Bucket=self.bucket_name, Key=f"{self.prefix}{filename}")
        file_content = res['Body'].read()
        return BytesIO(file_content)

class LocalFileStore(FileStore):
    def __init__(self, file_root_dir: Path = "/tmp/mais/file"):
        self.file_root_dir = file_root_dir
        os.makedirs(self.file_root_dir, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def _get_file_dir_path(self, filename: Path) -> Path:
        return self.file_root_dir / Path(filename.stem)

    def _get_file_path(self, filename: Path) -> Path:
        return self._get_file_dir_path(filename) / filename

    def store(self, filename: Path, content: IO[bytes]) -> str:
        # sanitize filename for secure fs storage
        filename = Path(secure_filename(str(filename)))
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

    def delete(self, filename: str) -> None:
        dir_path = self._get_file_dir_path(Path(filename))
        if dir_path.exists():
            self._rmtree(dir_path)

    def delete_all(self) -> None:
        for f in os.listdir(self.file_root_dir):
            self.logger.info(f"removing file {f}")
            self._rmtree(self.file_root_dir / Path(f))
    
    def _rmtree(self, path: str) -> None:
        shutil.rmtree(path, onexc=lambda func, path, exc_info: self.logger.warning(f"Error occurred while deleting {path}: {exc_info[1]}"))

    def get_url(self, filename: str) -> str:
        return f'/videos/{Path(filename).stem}/{filename}'
    
    def get_file(self, filename: str) -> IO[bytes]:
        return open(self._get_file_path(Path(filename)), 'rb')