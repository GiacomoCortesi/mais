from pydantic import BaseModel
from openapi_server.domain.models.id import ID
from typing import Any


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
    data: Any
    info: Info
    status: str
