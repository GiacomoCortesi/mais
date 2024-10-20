from typing import List
from openapi_server.domain.repositories.base_repository import BaseRepository
from openapi_server.domain.models.file import File
from openapi_server.domain.models.id import ID
import uuid
from typing import Dict


class FileRepository(BaseRepository[File]):
    pass


class InMemoryFileRepository(FileRepository):
    def __init__(self):
        self.files: Dict[ID, File] = {}

    def get_all(self) -> List[File]:
        return list(self.files.values())

    def get_by_id(self, id: ID) -> File:
        return self.files.get(id, None)

    def add(self, f: File) -> None:
        if not f.id:
            f.id = str(uuid.uuid())
        self.files[f.filename] = f

    def delete(self, id: ID) -> None:
        self.files.pop(id, None)

    def delete_all(self) -> None:
        self.files = {}

    def update(self, f: File) -> None:
        self.files[f.filename] = f
