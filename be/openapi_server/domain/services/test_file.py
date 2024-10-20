import unittest
from openapi_server.domain.models.transcription import Segment
from openapi_server.domain.services.file import FileService
from openapi_server.domain.repositories.file_repository import InMemoryFileRepository
from openapi_server.domain.services.file import InvalidFileException
from openapi_server.domain.services.file import AWSFileStore
from openapi_server.domain.services.file import LocalFileStore
from openapi_server.domain.services.file import RemotionFileRender
from unittest.mock import MagicMock
from faker import Faker
from openapi_server.domain.models.file import File
from pathlib import Path
import io

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


class TestFile(unittest.TestCase):
    file_repo = InMemoryFileRepository()
    file_store = LocalFileStore(file_root_dir=Path("/tmp/mais/file"))
    file_service = FileService(file_repo)

    def test_get_all(self):
        expected_files = [create_random_file() for _ in range(5)]
        self.file_repo.get_all = MagicMock(return_value=expected_files)
        files = self.file_service.get_all()
        self.assertEqual(files, expected_files)

    def test_get(self):
        expected_file = create_random_file()
        self.file_repo.get_by_id = MagicMock(return_value=expected_file)
        f = self.file_service.get("dummy")
        self.assertEqual(f, expected_file)

    def test_add_success(self):
        filename = Path("dummy.mov")
        content = io.BytesIO()
        content.write(b'dummy data')
        expected_file_path = self.file_store._get_file_path(filename)
        self.file_service.add(filename, content)
        self.assertTrue(expected_file_path.exists())

    def test_add_invalid_file(self):
        filename = Path("dummy.asdf")
        content = io.BytesIO()
        content.write(b'dummy data')
        with self.assertRaises(InvalidFileException):
            self.file_service.add(filename, content)

    def test_delete(self):
        filename = Path("dummy.mov")
        expected_file_path = self.file_store._get_file_path(filename)
        self.file_repo.delete = MagicMock(return_value=None)
        self.file_service.delete(filename)
        self.assertTrue(not expected_file_path.exists())

    def test_delete_all(self):
        self.file_repo.delete_all = MagicMock(return_value=None)
        self.file_service.delete_all()
        self.assertTrue(not any(self.file_store.file_root_dir.iterdir()))


@unittest.skip("may involve AWS costs, only run consciously")
class TestAWSFileStore(unittest.TestCase):
    def test_upload(self):
        file_store = AWSFileStore()
        content = b'\x00\x01\x02\x03' * 1024  # Example byte data
        content = io.BytesIO(content)
        filename = "mock-data"
        file_store.store(filename, content)

# @unittest.skip("may involve AWS costs, only run consciously")


class TestRemotionFileRender:
    def test_render(self):
        rf = RemotionFileRender()
        segments = [
            {
                'start': 1.099, 'end': 2.763, 'text': ' Cialo come il sole', 'words': [
                    {
                        'word': 'Cialo', 'start': 1.099, 'end': 1.4, 'score': 0.491}, {
                        'word': 'come', 'start': 1.58, 'end': 1.921, 'score': 0.587}, {
                        'word': 'il', 'start': 2.041, 'end': 2.081, 'score': 0.157}, {
                            'word': 'sole', 'start': 2.262, 'end': 2.763, 'score': 0.559}]}, {
                                'start': 4.238, 'end': 6.104, 'text': ' che mi scalda il cuore', 'words': [
                                    {
                                        'word': 'che', 'start': 4.238, 'end': 4.439, 'score': 0.253}, {
                                            'word': 'mi', 'start': 4.539, 'end': 4.619, 'score': 0.722}, {
                                                'word': 'scalda', 'start': 4.7, 'end': 5.302, 'score': 0.814}, {
                                                    'word': 'il', 'start': 5.402, 'end': 5.462, 'score': 0.814}, {
                                                        'word': 'cuore', 'start': 5.643, 'end': 6.104, 'score': 0.904}]}, {
                                                            'start': 7.556, 'end': 9.306, 'text': ' e blu come il mare.', 'words': [
                                                                {
                                                                    'word': 'e', 'start': 7.556, 'end': 7.616, 'score': 0.531}, {
                                                                        'word': 'blu', 'start': 7.737, 'end': 7.918, 'score': 0.709}, {
                                                                            'word': 'come', 'start': 8.079, 'end': 8.541, 'score': 0.774}, {
                                                                                'word': 'il', 'start': 8.682, 'end': 8.722, 'score': 0.255}, {
                                                                                    'word': 'mare.', 'start': 8.803, 'end': 9.306, 'score': 0.681}]}]
        segments = [Segment(**segment) for segment in segments]
        rf.render(
            video_url="https://music-ai-sub-upload-bucket.s3.amazonaws.com/uploads/conquista-cut.mp4",
            segments=segments)
