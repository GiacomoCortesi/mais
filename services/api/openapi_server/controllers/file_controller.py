import connexion

from services.file import InvalidFileException
from openapi_server.mappers.mappers import FileMapper
from pathlib import Path
from connexion.problem import problem
import io
from flask import send_file

from flask import current_app
from werkzeug.datastructures import FileStorage


def file_delete(filename=None):  # noqa: E501
    """Delete uploaded file(s)

     # noqa: E501

    :param filename: Filename of the video to be deleted, if no filename, all uploaded videos are deleted
    :type filename: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if filename:
        current_app.config['file_service'].delete(filename)
    else:
        current_app.config['file_service'].delete_all()


def file_get():  # noqa: E501
    """Retrieves the list of uploaded files

     # noqa: E501


    :rtype: Union[List[VideoGet200ResponseInner], Tuple[List[VideoGet200ResponseInner], int], Tuple[List[VideoGet200ResponseInner], int, Dict[str, str]]
    """
    video_files = current_app.config['file_service'].get_all()
    return [FileMapper.map_to_api(domain_file).to_dict() for domain_file in video_files], 200, {"Content-Type": "application/json"}

def file_id_get(id_):
    fs = current_app.config['file_service']
    return send_file(fs.get_file(id_), download_name=id_)

def file_post(file=None):
    """Uploads a audio or video file

     # noqa: E501

    :param file: 
    :type file: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if file.filename == '':
        return problem(
            title="BadRequest",
            detail="Filename missing",
            status=400)

    try:
        current_app.config['file_service'].add(
            Path(
                file.filename), io.BytesIO(
                file.stream.read()))
    except InvalidFileException:
        return problem(
            title="BadRequest",
            detail="Unsupported file format",
            status=400)
