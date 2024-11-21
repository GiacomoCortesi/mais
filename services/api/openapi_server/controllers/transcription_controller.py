import connexion

from services.file import RemotionFileRender
from openapi_server.models.transcription_request import TranscriptionRequest  # noqa: E501
from flask import current_app
import copy
from connexion.problem import problem
from services.transcription import TranscriptionNotFoundException
from flask import send_file
from connexion import request
from openapi_server.mappers.mappers import TranscriptionMapper


def transcription_get():  # noqa: E501
    """Fetch all transcriptions

     # noqa: E501


    :rtype: Union[List[Transcription], Tuple[List[Transcription], int], Tuple[List[Transcription], int, Dict[str, str]]
    """
    transcription_service = current_app.config['transcription_service']
    return [TranscriptionMapper.map_to_api(
        domain_transcription).to_dict() for domain_transcription in transcription_service.get_all()], 200, {"Content-Type": "application/json"}


def transcription_post(body):  # noqa: E501
    """Creates a new transcription
    NOTE: If you don't rename the transcription_post_request parameter into body, connexion will complain about
    the parameter being missing from the request. Inside job controller we do the same but it words, it may be
    a bug of connexion that depends on the openapi definition.
    May be related to: https://github.com/spec-first/connexion/issues/1939

     # noqa: E501

    :param transcription_post_request: 
    :type transcription_post_request: dict | bytes

    :rtype: Union[Transcription, Tuple[Transcription, int], Tuple[Transcription, int, Dict[str, str]]
    """
    body = TranscriptionRequest.from_dict(body)

    transcription_service = current_app.config['transcription_service']
    transcription = transcription_service.add(
        TranscriptionMapper.map_to_domain(body))

    return TranscriptionMapper.map_to_api(transcription).to_dict(), 200, {"Content-Type": "application/json"}


def transcription_id_clear_post(id_):  # noqa: E501
    """Restores initial transcription

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    transcription_service = current_app.config['transcription_service']
    try:
        current_transcription = transcription_service.get(id_)
    except TranscriptionNotFoundException:
        return problem(
            title="NotFound",
            detail="The requested transcription ID was not found on the server",
            status=404)
    transcription_service.edit(id_, copy.deepcopy(
        current_transcription.original_data))


def transcription_id_delete(id_):  # noqa: E501
    """Deletes a specific transcription

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    transcription_service = current_app.config['transcription_service']
    try:
        transcription_service.delete(id_)
    except TranscriptionNotFoundException:
        return problem(
            title="NotFound",
            detail="The requested transcription ID was not found on the server",
            status=404)


def transcription_id_patch(id_, body):  # noqa: E501
    """Edit a specific transcription

     # noqa: E501

    :param id:
    :type id: str
    :param transcription_id_patch_request:
    :type transcription_id_patch_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        body = TranscriptionRequest.from_dict(connexion.request.get_json())  # noqa: E501
    transcription_service = current_app.config['transcription_service']

    transcription_service.edit(
        id_, TranscriptionMapper.map_to_domain(body).data)


def transcription_id_fit_post(id_):  # noqa: E501
    """Fit start and end of each subtitles segment

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    transcription_service = current_app.config['transcription_service']
    transcription_service.fit(id_)


def transcription_id_fix_post(id_):  # noqa: E501
    """Attempts to fix all subtitles text with AI

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    transcription_service = current_app.config['transcription_service']
    transcription_service.fix(id_)


def transcription_id_get(id_):  # noqa: E501
    """Retrieves a specific transcription

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: Union[Transcription, Tuple[Transcription, int], Tuple[Transcription, int, Dict[str, str]]
    """
    transcription_service = current_app.config['transcription_service']
    try:
        transcription = transcription_service.get(id_)
    except TranscriptionNotFoundException:
        return problem(
            title="NotFound",
            detail="The requested transcription ID was not found on the server",
            status=404)

    return TranscriptionMapper.map_to_api(transcription).to_dict(), 200, {"Content-Type": "application/json"}


def transcription_id_export_get(id_, format=None):  # noqa: E501
    """Export transcription in several subtitle formats

     # noqa: E501

    :param id:
    :type id: str
    :param format: The format to export the transcription in
    :type format: str

    :rtype: Union[file, Tuple[file, int], Tuple[file, int, Dict[str, str]]
    """
    transcription_service = current_app.config['transcription_service']
    file_service = current_app.config['file_service']

    content = ""
    # needed because of https://github.com/spec-first/connexion/issues/1291

    try:
        if format == "stt":
            content = transcription_service.create_stt(id_)
            filename = f"{id_}.stt"
        elif format == "srt" or format is None:
            content = transcription_service.create_srt(id_)
            filename = f"{id_}.srt"
        elif format == "video":
            transcription = transcription_service.get(id_)
            f = file_service.get(transcription.filename)
            rfr = RemotionFileRender()
            filename = f"{id_}-render.mp4"
            content = rfr.render(video_url=f.video_url,
                                 segments=transcription.data.segments)
        else:
            return problem(title="BadRequest",
                           detail="Unsupported export format", status=400)
    except TranscriptionNotFoundException:
        return problem(
            title="NotFound",
            detail="The requested transcription ID was not found on the server",
            status=404)
    return send_file(content, download_name=filename, as_attachment=True)
