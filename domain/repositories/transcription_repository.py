from repositories.base_repository import BaseRepository
from models.transcription import Transcription
from models.id import ID
from typing import Dict, List
import uuid

class TranscriptionException(Exception):
    pass


class TranscriptionNotFoundException(TranscriptionException):
    def __init__(self, transcription_id: ID):
        self.message = f"Transcription with ID {transcription_id} not found"
        super().__init__(self.message)


class TranscriptionRepository(BaseRepository[Transcription]):
    pass


class InMemoryTranscriptionRepository(TranscriptionRepository):
    def __init__(self):
        self.transcriptions: Dict[ID, Transcription] = {}

    def get_all(self) -> List[Transcription]:
        return list(self.transcriptions.values())

    def get_by_id(self, id: ID) -> Transcription:
        t =  self.transcriptions.get(id, None)
        if not t:
            raise TranscriptionNotFoundException(id)
        return t

    def add(self, transcription: Transcription) -> None:
        if not transcription.id:
            transcription.id = str(uuid.uuid4())
        self.transcriptions[transcription.id] = transcription

    def delete(self, id: ID) -> None:
        try:
            self.transcriptions.pop(id)
        except KeyError:
            raise TranscriptionNotFoundException(id)

    def delete_all(self) -> None:
        self.transcriptions = {}

    def update(self, f: Transcription) -> None:
        self.transcriptions[f.id] = f
