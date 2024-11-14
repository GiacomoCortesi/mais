from openapi_server.domain.models.id import ID


class TranscriptionException(Exception):
    pass


class TranscriptionNotFoundException(TranscriptionException):
    def __init__(self, transcription_id: ID):
        self.message = f"Transcription with ID {transcription_id} not found"
        super.__init__(self.message)


class SubtitleServiceException(Exception):
    pass


class FileException(Exception):
    pass


class FileNotFoundException(FileException):
    def __init__(self, file_id: ID):
        self.message = f"File with ID {file_id} not found"

class FileServiceException(Exception):
    pass


class InvalidFileException(FileServiceException):
    def __init__(self, filename: str):
        self.message = f"File {filename} extension not supported"


class FileStoreException(Exception):
    pass


class FileRenderException(Exception):
    pass

class JobNotFoundException(Exception):
    pass
