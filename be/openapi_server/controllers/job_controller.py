import connexion

from openapi_server.models.job_request import JobRequest  # noqa: E501
from openapi_server.models.job_response import JobResponse  # noqa: E501

from openapi_server.domain.services.subtitle import SubtitleService
from openapi_server.domain.services.job import JobNotFoundException
from openapi_server.mappers.mappers import JobMapper
from flask import current_app

from connexion.problem import problem


def job_get():  # noqa: E501
    """Get all job details

     # noqa: E501


    :rtype: Union[List[JobResponse], Tuple[List[JobResponse], int], Tuple[List[JobResponse], int, Dict[str, str]]
    """
    job_service = current_app.config['job_service']
    jobs = job_service.get_all()
    return [JobMapper.map_to_api(domain_job) for domain_job in jobs], 200


def job_id_get(id_):  # noqa: E501
    """Get job details

     # noqa: E501

    :param id:
    :type id: str

    :rtype: Union[JobResponse, Tuple[JobResponse, int], Tuple[JobResponse, int, Dict[str, str]]
    """
    job_service = current_app.config['job_service']
    try:
        job = job_service.get(id_)
    except JobNotFoundException:
        return problem(
            title="NotFound",
            detail="The requested job ID was not found on the server",
            status=404)
    return JobMapper.map_to_api(job)


def job_post(job_request=None):  # noqa: E501
    """Create a new subtitles generation job

     # noqa: E501

    :param job_request: 
    :type job_request: dict | bytes

    :rtype: Union[JobResponse, Tuple[JobResponse, int], Tuple[JobResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        mais_job_post_request = JobRequest.from_dict(connexion.request.get_json())  # noqa: E501

    if mais_job_post_request.config:
        subtitle_service = SubtitleService(
            model_size=mais_job_post_request.config.model_size,
            language=mais_job_post_request.config.language)
    else:
        subtitle_service = SubtitleService()

    job_service = current_app.config['job_service']
    current_app.config['file_service']

    job_info = {
        "filename": mais_job_post_request.filename,
        "config": {
            "speaker_detection": subtitle_service.speaker_detection,
            "subtitles_frequency": subtitle_service.subtitles_frequency,
            "language": subtitle_service.language,
            "model_size": subtitle_service.model_size}}
    # video = file_service.get(mais_job_post_request.filename)
    # TODO: eventyally handle subtitle generation in the job runner with a specific task. Multiple jobs that depend on each other? (e.g. subtitle gen job depends on vocal extraction etc.)
    # job = job_service.run(job_info, subtitle_service.generate_subtitles, video["video_path"])
    job = job_service.run(job_info, subtitle_service.generate_subtitles_mock)
    return JobMapper.map_to_api(job)
