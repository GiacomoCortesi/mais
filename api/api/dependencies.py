import os
from api.repositories.file import InMemoryFileRepository, FileRepository, FileStore, AWSFileStore
from api.repositories.transcription import InMemoryTranscriptionRepository, TranscriptionRepository
from api.services.file import FileService
from fastapi import Depends
import redis

from api.services.job import JobService
from api.services.transcription import TranscriptionService

file_repository = InMemoryFileRepository()
file_store = AWSFileStore()


redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

def get_file_repository() -> FileRepository:
    return file_repository

def get_file_store() -> FileStore:
    return file_store

def get_file_service(
    repo: FileRepository = Depends(get_file_repository),
    store: FileStore = Depends(get_file_store),
) -> FileService:
    return FileService(repo, store)
transcription_repository = InMemoryTranscriptionRepository()

def get_transcription_repository() -> TranscriptionRepository:
    return transcription_repository

def get_transcription_service(
        repo: TranscriptionRepository = Depends(get_transcription_repository)
) -> TranscriptionService:
    return TranscriptionService(os.getenv("OPENAI_API_TOKEN", ""), repo)

def get_redis_client() -> redis.Redis:
    return redis_client

def get_job_service(redis_client = Depends(get_redis_client)):
    return JobService(redis_client)