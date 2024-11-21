import connexion

from openapi_server.models.job_request import JobRequest  # noqa: E501
from openapi_server.models.job_response import JobResponse  # noqa: E501

from services.job import JobNotFoundException
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
    return [JobMapper.map_to_api(domain_job) for domain_job in jobs], 200, {"Content-Type": "application/json"}


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
    return JobMapper.map_to_api(job).to_dict(), 200, {"Content-Type": "application/json"}


def job_post(body=None):  # noqa: E501
    """Create a new subtitles generation job

     # noqa: E501

    :param job_request: 
    :type job_request: dict | bytes

    :rtype: Union[JobResponse, Tuple[JobResponse, int], Tuple[JobResponse, int, Dict[str, str]]
    """
    job_service = current_app.config['job_service']
    current_app.config['file_service']
    # video = file_service.get(mais_job_post_request.filename)
    # TODO: eventyally handle subtitle generation in the job runner with a specific task. Multiple jobs that depend on each other? (e.g. subtitle gen job depends on vocal extraction etc.)
    # job = job_service.run(job_info, subtitle_service.generate_subtitles, video["video_path"])
    job = job_service.run(**body)
    return JobMapper.map_to_api(job).to_dict(), 200, {"Content-Type": "application/json"}
