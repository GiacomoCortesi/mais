from pydantic import BaseModel


class Config(BaseModel):
    model_size: str
    subtitles_frequency: int
    language: str
    speaker_detection: bool
    hugging_face_token: str
