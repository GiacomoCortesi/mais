![GitHub commit activity](https://img.shields.io/github/commit-activity/m/GiacomoCortesi/music-ai-sub)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1vGiYb6ODdaRhMo6KMXC3lSFDkTCU1jc_?usp=sharing)

# music-ai-sub
AI-powered app for transcribing music lyric videos into multiple subtitle formats (e.g. srt, vtt) with an integrated editor for smart and simplified subtitle modifications.

Note that this is a full stack app where:
 - frontend side is built upon Next js with nextui and tailwind for styling
 - web server is API first, code stubs generated through openapi generator CLI for python flask with connexion library
 - AI services use whisperx for subtitles generation, spleeter for audio to stems separation, and ChatGPT for smart subtitle fixes.

Main features:
 - whisperx speech-to-text and diarization
 - spleeter vocals extraction
 - redis queue for generation jobs management
 - smart subtitles editor

 [MAIS Architecture](https://ibb.co/x35TZrn)

# Run & Develop
## UI
```bash
cd ui
npm install
npm run dev
```
## Backend
Prerequisites:
 - install and start redis stack (e.g. with [docker](https://hub.docker.com/_/redis/))
 - start redis queue worker process:
  `rq worker --with-scheduler`

Run:
```bash
cd be
python3 -m openapi_server
```

### Generate code stubs with openapi CLI generator tool
With Docker:

```bash
cd be

docker run --rm -v "${PWD}:/local"  -v /home/gcortesi/music-ai-sub/openapi.yml:/openapi.yml openapitools/openapi-generator-cli generate    -i /openapi.yml     -g python-flask     -o /local/
```

Check [selective-generation](https://openapi-generator.tech/docs/customization/#selective-generation) documentation to only select desired code generation pieces.

The project use .openapi-generator-ignore to selectively exclude files from generation.  
By default only the openapi spec and the models are regenerated, make sure to tweak the file as needed before regenerating
code stubs.

### Testing
Run all backend unit tests with pytest:
```
cd be
pytest --cov=openapi_server
```

Selectively run tests with pytest:
```
pytest be/openapi_server/test/test_job_controller.py::TestJobController
```

Run all backend unit tests with tox:
```
tox run
```