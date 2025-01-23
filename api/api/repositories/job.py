from api.repositories.base import BaseRepository, NotFoundException
from api.models import JobResponse as Job
from typing import Dict, List
import uuid

class JobNotFoundException(NotFoundException):
    def __init__(self, job_id: str):
        self.message = f"Job with ID {job_id} not found"
        super().__init__(self.message)


class JobRepository(BaseRepository[Job]):
    pass


class InMemoryJobRepository(JobRepository):
    def __init__(self):
        self.jobs: Dict[str, Job] = {}

    def get_all(self) -> List[Job]:
        return list(self.jobs.values())

    def get_by_id(self, id: str) -> Job:
        t =  self.jobs.get(id, None)
        if not t:
            raise JobNotFoundException(id)
        return t

    def add(self, job: Job) -> None:
        if not job.id:
            job.id = str(uuid.uuid4())
        self.jobs[job.id] = job

    def delete(self, id: str) -> None:
        try:
            self.jobs.pop(id)
        except KeyError:
            raise JobNotFoundException(id)

    def delete_all(self) -> None:
        self.jobs = {}

    def update(self, f: Job) -> None:
        self.jobs[f.id] = f
