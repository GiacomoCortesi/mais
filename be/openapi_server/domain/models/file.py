from pydantic import BaseModel
from datetime import datetime


class File(BaseModel):
    filename: str
    id: str
    video_url: str
    image_url: str
    upload_date: datetime
