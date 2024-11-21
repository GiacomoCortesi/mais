import unittest
from unittest.mock import MagicMock

from flask import json

from openapi_server.models.job_request import JobRequest
from openapi_server.test import BaseTestCase

from services.job import JobNotFoundException
from services.job import Job as DomainJob


class TestJobController(BaseTestCase):
    """JobController integration test stubs"""
    job_config_mock = {
        "speaker_detection": True,
        "subtitles_frequency": 5,
        "language": "language",
        "model_size": "model_size"}
    job_mock = {
        "id": "test-job",
        "data": "",
        "info": {
            "filename": "somefile",
            "config": job_config_mock},
        "status": "started"}

    def test_job_get(self):
        """Test case for job_get

        Get all job details
        """
        headers = {
            'Accept': 'application/json',
        }
        js = self.app.config['job_service']

        test_cases = [{"name": "no_jobs",
                       "mock_return_value": [],
                       "expected_result": []},
                      {"name": "with_jobs",
                       "mock_return_value": [DomainJob(**self.job_mock)],
                       "expected_result": [self.job_mock]}]
        for test_case in test_cases:
            with self.subTest(case=test_case):
                js.get_all = MagicMock(
                    return_value=test_case["mock_return_value"])
                response = self.client.open(
                    '/job',
                    method='GET',
                    headers=headers)
                self.assertEqual(response.json, test_case["expected_result"])
                self.assert200(
                    response,
                    'Response body is : ' +
                    response.data.decode('utf-8'))

    def test_job_id_get(self):
        """Test case for job_id_get

        Get job details
        """
        headers = {
            'Accept': 'application/json',
        }
        js = self.app.config['job_service']
        job_id = self.job_mock["id"]
        test_cases = [{"name": "job_id_does_not_exist",
                       "mock_return_value": None,
                       "expected_result": None,
                       "mock_side_effect": JobNotFoundException()},
                      {"name": "job_id_exist",
                       "mock_return_value": DomainJob(**self.job_mock),
                       "expected_result": self.job_mock,
                       "mock_side_effect": None}]
        for test_case in test_cases:
            with self.subTest(case=test_case):
                js.get = MagicMock(
                    return_value=test_case["mock_return_value"],
                    side_effect=test_case["mock_side_effect"])
                response = self.client.open(
                    '/job/{job_id}'.format(job_id=job_id),
                    method='GET',
                    headers=headers)
                if test_case["mock_side_effect"] is not None:
                    self.assert404(
                        response,
                        'Response body is : ' +
                        response.data.decode('utf-8'))
                else:
                    self.assertEqual(
                        response.json, test_case["expected_result"])
                    self.assert200(
                        response,
                        'Response body is : ' +
                        response.data.decode('utf-8'))

    def test_job_post(self):
        """Test case for job_post

        Create a new subtitles generation job
        """
        job_request = JobRequest(
            **{"filename": "file", "config": self.job_config_mock})
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        js = self.app.config['job_service']

        js.run = MagicMock(return_value=DomainJob(**self.job_mock))

        response = self.client.open(
            '/job',
            method='POST',
            headers=headers,
            data=json.dumps(job_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
