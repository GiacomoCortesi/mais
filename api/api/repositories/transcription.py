from api.repositories.base import BaseRepository, NotFoundException
from api.models import TranscriptionResponse as Transcription
from typing import Dict, List
import uuid

class TranscriptionNotFoundException(NotFoundException):
    def __init__(self, transcription_id: str):
        self.message = f"Transcription with ID {transcription_id} not found"
        super().__init__(self.message)


class TranscriptionRepository(BaseRepository[Transcription]):
    pass


class InMemoryTranscriptionRepository(TranscriptionRepository):
    def __init__(self):
        self.transcriptions: Dict[str, Transcription] = {}

    def get_all(self) -> List[Transcription]:
        return list(self.transcriptions.values())

    def get_by_id(self, id: str) -> Transcription:
        t =  self.transcriptions.get(id, None)
        if not t:
            raise TranscriptionNotFoundException(id)
        return t

    def add(self, transcription: Transcription) -> None:
        self.transcriptions[transcription.id] = transcription

    def delete(self, id: str) -> None:
        try:
            self.transcriptions.pop(id)
        except KeyError:
            raise TranscriptionNotFoundException(id)

    def delete_all(self) -> None:
        self.transcriptions = {}

    def update(self, f: Transcription) -> None:
        self.transcriptions[f.id] = f
