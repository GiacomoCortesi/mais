from fastapi import APIRouter, File, Path, Query, UploadFile, Depends
from typing import List, Optional
from api.models import FileResponse
from api.dependencies import get_file_service
from fastapi.responses import StreamingResponse

file_router = APIRouter()

@file_router.get("/file", response_model=List[FileResponse])
def get_files(service=Depends(get_file_service)):
    return service.get_all()

@file_router.post("/file", response_model=FileResponse)
def upload_file(file: UploadFile = File(...), service=Depends(get_file_service)):
    return service.add(file.filename, file.file)

@file_router.delete("/file")
def delete_files(filename: Optional[str] = Query(None, description="Filename to delete"), service=Depends(get_file_service)):
    if filename:
        return service.delete(filename)
    return service.delete_all()

@file_router.get("/file/{id}", response_model=FileResponse)
def get_file_by_id(id: str = Path(..., description="File ID"), service=Depends(get_file_service)):
    file_obj = service.get_file(id)
    return StreamingResponse(file_obj, media_type="application/octet-stream", headers={
            "Content-Disposition": f"attachment; filename={id}"
        })
