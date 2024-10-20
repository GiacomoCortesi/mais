from openapi_server.domain.repositories.base_repository import BaseRepository
from openapi_server.domain.models.transcription import Transcription
from openapi_server.domain.models.id import ID
from typing import Dict, List
import uuid


class TranscriptionRepository(BaseRepository[Transcription]):
    pass


class InMemoryTranscriptionRepository(TranscriptionRepository):
    def __init__(self):
        self.transcriptions: Dict[ID, Transcription] = {}

    def get_all(self) -> List[Transcription]:
        return list(self.transcriptions.values())

    def get_by_id(self, id: ID) -> Transcription:
        return self.transcriptions.get(id, None)

    def add(self, transcription: Transcription) -> None:
        if not transcription.id:
            transcription.id = str(uuid.uuid())
        self.transcriptions[transcription.id] = transcription

    def delete(self, id: ID) -> None:
        self.transcriptions.pop(id, None)

    def delete_all(self) -> None:
        self.transcriptions = {}

    def update(self, f: Transcription) -> None:
        self.transcriptions[f.id] = f
