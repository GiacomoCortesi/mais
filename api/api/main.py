import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.repositories.base import NotFoundException
from api.routers.file import file_router
from api.routers.job import job_router
from api.routers.transcription import transcription_router
from api.services.file import RemotionFileRender


from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Add CORS middleware to allow all origins, headers, and methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )

@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"error": exc.message},
    )

app.include_router(file_router, tags=["file"])
app.include_router(job_router, tags=["job"])
app.include_router(transcription_router, tags=["transcription"])