import logging

import connexion
from flask_testing import TestCase

from openapi_server.encoder import JSONEncoder
from openapi_server.domain.services.job import JobService
from openapi_server.domain.services.file import FileService
from openapi_server.domain.services.transcription import TranscriptionService
from fakeredis import FakeStrictRedis
import os


class BaseTestCase(TestCase):
    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../openapi/')
        app.app.json_encoder = JSONEncoder
        app.add_api('openapi.yaml', pythonic_params=True)
        js = JobService(FakeStrictRedis())
        app.app.config.update({
            'file_service': FileService(),
            'job_service': js,
            'transcription_service': TranscriptionService(os.environ.get('OPENAI_TOKEN', ""))
        })
        return app.app
