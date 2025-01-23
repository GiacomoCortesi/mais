from fastapi import APIRouter, Path, Depends
from typing import List
from api.dependencies import get_job_service
from api.models import JobRequest, JobResponse

job_router = APIRouter()

@job_router.get("/job", response_model=List[JobResponse])
def get_jobs(service=Depends(get_job_service)):
    return service.get_all()

@job_router.post("/job", response_model=JobResponse)
def create_job(job_request: JobRequest, service=Depends(get_job_service)):
    return service.run(job_request)

@job_router.get("/job/{id}", response_model=JobResponse)
def get_job_by_id(id: str = Path(..., description="Job ID"), service=Depends(get_job_service)):
    return service.get(id)