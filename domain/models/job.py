from pydantic import BaseModel
from models.id import ID
from typing import Any, Optional


class Config(BaseModel):
    model_size: str
    subtitles_frequency: int
    language: str
    speaker_detection: bool


class Info(BaseModel):
    filename: str
    config: Config


class Job(BaseModel):
    id: ID
    data: Optional[Any] = {}
    info: Info
    status: Optional[str] = ""
