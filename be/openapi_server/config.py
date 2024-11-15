from openapi_server.domain.services.job import JobService
from openapi_server.domain.services.file import FileService
from openapi_server.domain.repositories.file_repository import AWSFileStore
from openapi_server.domain.services.transcription import TranscriptionService
import os
from redis import Redis


def get_config():
    r = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))
    return {
        'file_service': FileService(
            file_store=AWSFileStore()),
        'job_service': JobService(r),
        'transcription_service': TranscriptionService(
            os.environ.get(
                'OPENAI_TOKEN',
                ""))}
