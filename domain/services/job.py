from models.job import Job, Info
from typing import List, Any
from redis import Redis
import uuid
import json

class JobNotFoundException(Exception):
    pass

class JobService:
    def __init__(self, redis_client: Redis):
        self.r = redis_client

    def get_all(self) -> List[Job]:
        all_jobs = []
        for job_id in self.r.lrange('subtitle', 0, -1):
            job_info = self.r.json().get(f'job:{job_id.decode()}')
            all_jobs.append(job_info)
        return all_jobs

    def get(self, job_id) -> Job:
        job = self.r.json().get(f'job:{job_id}')

        if job is None:
            raise JobNotFoundException

        return Job(**job)

    def run(self, job_type: str = 'subtitle', **kwargs) -> Job:
        job_id = str(uuid.uuid4())
        job_info = Info(**kwargs)
        job = Job(id=job_id, info=job_info, status='queued')

        self.r.json().set(f'job:{job_id}', '$', job.model_dump())
        self.r.rpush(job_type, job_id)

        return job
