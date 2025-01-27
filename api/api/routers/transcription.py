import copy
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.responses import StreamingResponse
from api.dependencies import get_file_service, get_transcription_service
from api.models import TranscriptionRequest, TranscriptionResponse
from api.services.file import RemotionFileRender

transcription_router = APIRouter()

@transcription_router.get("/transcription", response_model=List[TranscriptionResponse])
def get_transcriptions(service=Depends(get_transcription_service)):
    return service.get_all()

@transcription_router.post("/transcription", response_model=TranscriptionResponse)
def create_transcription(transcription_request: TranscriptionRequest, service=Depends(get_transcription_service)):
    return service.add(transcription_request)

@transcription_router.get("/transcription/{id}", response_model=TranscriptionResponse)
def get_transcription_by_id(id: str = Path(..., description="Transcription ID"), service=Depends(get_transcription_service)):
    return service.get(id)

@transcription_router.delete("/transcription/{id}")
def delete_transcription(id: str = Path(..., description="Transcription ID"), service=Depends(get_transcription_service)):
    service.delete(id)

@transcription_router.patch("/transcription/{id}")
def patch_transcription(transcription_request: TranscriptionRequest, id: str = Path(..., description="Transcription ID"), service=Depends(get_transcription_service)):
    return service.edit(id, transcription_request)

@transcription_router.post("/transcription/{id}/clear")
def transcription_id_clear(
    id: str = Path(..., description="Transcription ID"),
    service=Depends(get_transcription_service)
):
    """
    Restores initial transcription.
    """
    current_transcription = service.get(id)
    current_transcription.data = copy.deepcopy(current_transcription.original_data)
    service.edit(id, copy.deepcopy(current_transcription))


@transcription_router.post("/transcription/{id}/fit")
def transcription_id_fit(
    id: str = Path(..., description="Transcription ID"),
    service=Depends(get_transcription_service)
):
    """
    Fit start and end of each subtitle segment.
    """
    service.fit(id)


@transcription_router.post("/transcription/{id}/fix")
def transcription_id_fix(
    id: str = Path(..., description="Transcription ID"),
    service=Depends(get_transcription_service)
):
    """
    Attempts to fix all subtitle text with AI.
    """
    service.fix(id)


@transcription_router.get("/transcription/{id}/export")
def transcription_id_export(
    id: str = Path(..., description="Transcription ID"),
    format: str = Query(None, description="Export format (stt, srt, video)"),
    service=Depends(get_transcription_service),
    file_service=Depends(get_file_service)  # Assume get_file_service is a dependency
):
    """
    Export transcription in several subtitle formats.
    """
    content = ""
    filename = ""
    if format == "stt":
        content = service.create_stt(id)
        filename = f"{id}.vtt"
    elif format == "srt" or format is None:
        content = service.create_srt(id)
        filename = f"{id}.srt"
    elif format == "video":
        transcription = service.get(id)
        f = file_service.get(transcription.filename)
        rfr = RemotionFileRender()
        filename = f"{id}-render.mp4"
    
        content = rfr.render(
            video_url=f.video_url,
            segments=transcription.data.segments,
            width=f.width,
            height=f.height,
            duration=f.duration,
            subtitle_config=transcription.subtitle_config
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported export format"
        )
    
    return StreamingResponse(
        content,
        media_type="video/mp4",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


