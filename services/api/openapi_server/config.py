from services.job import JobService
from services.file import FileService
from repositories.file_repository import LocalFileStore
from services.transcription import TranscriptionService
import os
from redis import Redis


def get_config():
    r = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))
    return {
        'file_service': FileService(
            file_store=LocalFileStore()),
        'job_service': JobService(r),
        'transcription_service': TranscriptionService(
            os.environ.get(
                'OPENAI_TOKEN',
                ""))
                }
