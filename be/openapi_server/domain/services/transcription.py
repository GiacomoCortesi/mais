import io
import requests
import uuid
import json
import copy
from datetime import timedelta
from openapi_server.domain.repositories.transcription_repository import TranscriptionRepository
from openapi_server.domain.repositories.transcription_repository import InMemoryTranscriptionRepository
from openapi_server.domain.models.transcription import Transcription
from openapi_server.domain.models.id import ID
from typing import IO, List


class TranscriptionNotFoundException(Exception):
    pass


class TranscriptionService:
    def __init__(
            self,
            openai_token,
            repository: TranscriptionRepository = None):
        self.openai_token = openai_token
        if not repository:
            repository = InMemoryTranscriptionRepository()
        self.repository = repository

    def add(self, transcription: Transcription):
        transcription_id = str(uuid.uuid4())
        transcription.id = transcription_id
        transcription.original_data = copy.deepcopy(transcription.data)
        self.repository.add(transcription)

        return transcription

    def get_all(self) -> List[Transcription]:
        return self.repository.get_all()

    def get(self, id: ID) -> Transcription:
        transcription = self.repository.get_by_id(id)
        if not transcription:
            raise TranscriptionNotFoundException
        return transcription

    def edit(self, id, transcription_data):
        transcription = self.get(id)
        transcription.data = transcription_data
        self.repository.update(transcription)

    def delete(self, id):
        try:
            self.repository.delete(id)
        except KeyError:
            raise TranscriptionNotFoundException

    def fit(self, id):
        transcription = self.get(id)
        segments = copy.deepcopy(transcription.data.segments)
        for index, segment in enumerate(segments):
            if index == 0:
                segment_start = 0
            else:
                segment_start = segments[index - 1].end
            segment_end = segment.end

            segment.start = segment_start
            segment.end = segment_end

        transcription.data.segments = segments

        self.edit(id, transcription.data)
        return transcription

    def fix(self, id) -> None:
        transcription = self.get(id)
        transcription_data = transcription.data
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_token}"
        }
        prompt = f'''
        The following data contains some text in {transcription_data.language} language code.
        The text may contain incorrect words, attempt to fix incorrect words.
        The text you need to consider is inside the segments array, each element in the array has a text field
        containing the target text. When doing the correction you can try to make meaningful corrections also based on the
        overall context of the text.
        Try to correct as little as possible.
        There may be some word in a different language (or wrongly translated), fix it in the original language but do not translate it.
        Only respond in valid JSON format
        In the returned JSON skip the "word_segments" and "language" keys. Only include the "segments" key.
        In the "segments" object skip the "words" key.
        {transcription_data}
        '''
        data = {
            "response_format": {"type": "json_object"},
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=data)
        if not response.ok:
            return

        response_data = response.json()
        segments = json.loads(
            response_data["choices"][0]["message"]["content"])["segments"]

        for index, segment in enumerate(segments):
            if index < len(transcription.data.segments):
                transcription.data.segments[index].text = segment.get(
                    "text", "")

        self.edit(id, transcription.data)

    def create_vtt(self, id) -> IO[bytes]:
        transcription = self.get(id)
        stt_content = ""
        for index, segment in enumerate(transcription.data.segments):
            start_time = self.format_time(segment.start)
            end_time = self.format_time(segment.end)
            text = segment.text
            stt_content += f"{index}\n{start_time} --> {end_time}\n{text}\n\n"

        return io.BytesIO(stt_content.encode())

    def create_srt(self, id) -> IO[bytes]:
        transcription = self.get(id)
        srt_content = ""
        for index, segment in enumerate(transcription.data.segments):
            start_time = self.format_time(segment.start)
            end_time = self.format_time(segment.end)
            text = segment.text
            srt_content += f"{index + 1}\n{start_time} --> {end_time}\n{text}\n\n"

        return io.BytesIO(srt_content.encode())

    @staticmethod
    def format_time(seconds):
        td = timedelta(seconds=seconds)
        return str(td)[:-3].replace('.', ',')
