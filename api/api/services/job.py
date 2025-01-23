from api.models import JobRequest, JobResponse
from typing import List
from redis import Redis
import uuid

from api.repositories.base import NotFoundException

class JobNotFoundException(NotFoundException):
    pass

class JobService:
    def __init__(self, redis_client: Redis):
        self.r = redis_client

    def get_all(self) -> List[JobResponse]:
        all_jobs = []
        for job_id in self.r.lrange('subtitle', 0, -1):
            job_info = self.r.json().get(f'job:{job_id.decode()}')
            all_jobs.append(job_info)
        return all_jobs

    def get(self, job_id) -> JobResponse:
        job = self.r.json().get(f'job:{job_id}')

        if job is None:
            raise JobNotFoundException

        return JobResponse(**job)

    def run(self, job_request: JobRequest) -> JobResponse:
        id = job_request.id if job_request.id else str(uuid.uuid4())
        job = JobResponse(id=id, info=job_request.info, status='pending')

        self.r.json().set(f'job:{id}', '$', job.model_dump())
        self.r.rpush('subtitle', id)

        return job
