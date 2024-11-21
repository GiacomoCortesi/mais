import unittest


from models.file import File
from openapi_server.test import BaseTestCase
from unittest.mock import MagicMock
from faker import Faker

fake = Faker()


def create_random_file() -> File:
    return File(
        filename=fake.word(),
        id=fake.uuid4(),
        video_url=fake.url(),
        image_url=fake.url(),
        upload_date=fake.date_time_this_decade(),
        video_path=fake.file_path(),
        image_path=fake.file_path()
    )


class TestFileController(BaseTestCase):
    """FileController integration test stubs"""

    def test_file_get(self):
        """Test case for file_get

        Retrieves the list of uploaded videos
        """
        headers = {
            'Accept': 'application/json',
        }

        vs = self.app.config["file_service"]
        vs.get = MagicMock(return_value=[create_random_file()])

        response = self.client.open(
            '/file',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_file_post(self):
        """Test case for file_post

        Uploads a video or audio file
        """
        headers = {
            'Content-Type': 'multipart/form-data',
        }
        data = dict(file='/path/to/file')
        response = self.client.open(
            '/file',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
