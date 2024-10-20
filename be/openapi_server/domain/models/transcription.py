from pydantic import BaseModel
from openapi_server.domain.models.id import ID

from typing import List, Optional


class Word(BaseModel):
    word: str
    start: float
    end: float
    score: float


class Segment(BaseModel):
    start: float
    end: float
    text: str
    words: List[Word]


class TranscriptionData(BaseModel):
    segments: List[Segment]
    word_segments: List[Word]
    language: str


class Transcription(BaseModel):
    id: Optional[ID] = None
    data: TranscriptionData
    original_data: Optional[TranscriptionData] = None
    job_id: Optional[ID] = None
    filename: Optional[str] = None
