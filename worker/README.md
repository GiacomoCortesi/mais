## MAIS Worker

MAIS Worker fetches transcription jobs from a redis queue and use WhisperX and demucs to generate transcriptions

Require hugging face token, see [whisperx Speaker Diarization section](https://github.com/m-bain/whisperX)

Requires ffmpeg to be installed

### Run With Docker
Build the worker docker image

`docker build -t mais-worker .`

Run the docker image

`docker run --rm mais-worker`

### Configuration
mais worker can be configured through the following environment variables:

```
REDIS_HOST=redis-server
REDIS_PORT=6379
API_HOST=api-server
API_PORT=8000
```