import logging

import connexion
from flask_testing import TestCase

from services.job import JobService
from services.file import FileService
from services.transcription import TranscriptionService
from fakeredis import FakeStrictRedis
import os


class BaseTestCase(TestCase):
    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../openapi/')
        app.add_api('openapi.yaml', pythonic_params=True)
        js = JobService(FakeStrictRedis())
        app.app.config.update({
            'file_service': FileService(),
            'job_service': js,
            'transcription_service': TranscriptionService(os.environ.get('OPENAI_TOKEN', ""))
        })
        return app.app
