from io import BytesIO
import unittest
from unittest.mock import MagicMock
from services.transcription import TranscriptionService
from models.transcription import Transcription


class TestTranscription(unittest.TestCase):
    def test_fit(self):
        transcription_mock_success = {
            'original_data': None, 'transcription_id': 'dummy', 'job_id': "dummy_job_id", 'video_file': 'dummy_file.mov', 'data': {
                'segments': [
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
                                                                                            'word': 'mare.', 'start': 8.803, 'end': 9.306, 'score': 0.681}]}], 'word_segments': [], 'language': 'it'}}
        transcription_mock_success_expected = Transcription(
            **{
                'original_data': None, 'transcription_id': 'dummy', 'job_id': "dummy_job_id", 'video_file': 'dummy_file.mov', 'data': {
                    'segments': [
                        {
                            'start': 0, 'end': 2.763, 'text': ' Cialo come il sole', 'words': [
                                {
                                    'word': 'Cialo', 'start': 1.099, 'end': 1.4, 'score': 0.491}, {
                                    'word': 'come', 'start': 1.58, 'end': 1.921, 'score': 0.587}, {
                                    'word': 'il', 'start': 2.041, 'end': 2.081, 'score': 0.157}, {
                                        'word': 'sole', 'start': 2.262, 'end': 2.763, 'score': 0.559}]}, {
                                            'start': 2.763, 'end': 6.104, 'text': ' che mi scalda il cuore', 'words': [
                                                {
                                                    'word': 'che', 'start': 4.238, 'end': 4.439, 'score': 0.253}, {
                                                        'word': 'mi', 'start': 4.539, 'end': 4.619, 'score': 0.722}, {
                                                            'word': 'scalda', 'start': 4.7, 'end': 5.302, 'score': 0.814}, {
                                                                'word': 'il', 'start': 5.402, 'end': 5.462, 'score': 0.814}, {
                                                                    'word': 'cuore', 'start': 5.643, 'end': 6.104, 'score': 0.904}]}, {
                                                                        'start': 6.104, 'end': 9.306, 'text': ' e blu come il mare.', 'words': [
                                                                            {
                                                                                'word': 'e', 'start': 7.556, 'end': 7.616, 'score': 0.531}, {
                                                                                    'word': 'blu', 'start': 7.737, 'end': 7.918, 'score': 0.709}, {
                                                                                        'word': 'come', 'start': 8.079, 'end': 8.541, 'score': 0.774}, {
                                                                                            'word': 'il', 'start': 8.682, 'end': 8.722, 'score': 0.255}, {
                                                                                                'word': 'mare.', 'start': 8.803, 'end': 9.306, 'score': 0.681}]}], 'word_segments': [], 'language': 'it'}})
        service = TranscriptionService("")
        service.get = MagicMock(
            return_value=Transcription(
                **transcription_mock_success))
        self.assertEqual(
            service.fit("dummy"),
            transcription_mock_success_expected)

    def test_create_srt(self):
        transcription_mock = {
            'original_data': None, 'transcription_id': 'dummy', 'job_id': "dummy_job_id", 'video_file': 'dummy_file.mov', 'data': {
                'segments': [
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
                                                                                            'word': 'mare.', 'start': 8.803, 'end': 9.306, 'score': 0.681}]}], 'word_segments': [], 'language': 'it'}}
        expected = BytesIO(b"1\n0:00:01,099 --> 0:00:02,763\n Cialo come il sole\n\n2\n0:00:04,238 --> 0:00:06,104\n che mi scalda il cuore\n\n3\n0:00:07,556 --> 0:00:09,306\n e blu come il mare.\n\n")
        service = TranscriptionService("")
        service.get = MagicMock(
            return_value=Transcription(
                **transcription_mock))
        srt_content = service.create_srt("dummy_id")
        self.assertEqual(srt_content.getvalue(), expected.getvalue())

    def test_create_stt(self):
        transcription_mock = {
            'original_data': None, 'transcription_id': 'dummy', 'job_id': "dummy_job_id", 'video_file': 'dummy_file.mov', 'data': {
                'segments': [
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
                                                                                            'word': 'mare.', 'start': 8.803, 'end': 9.306, 'score': 0.681}]}], 'word_segments': [], 'language': 'it'}}
        expected = BytesIO(b"0\n0:00:01,099 --> 0:00:02,763\n Cialo come il sole\n\n1\n0:00:04,238 --> 0:00:06,104\n che mi scalda il cuore\n\n2\n0:00:07,556 --> 0:00:09,306\n e blu come il mare.\n\n")
        service = TranscriptionService("")
        service.get = MagicMock(
            return_value=Transcription(
                **transcription_mock))
        stt_content = service.create_vtt("dummy_id")
        self.assertEqual(stt_content.getvalue(), expected.getvalue())
