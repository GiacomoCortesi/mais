FROM python:3.10.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt /app

RUN pip3 install --no-cache-dir -r requirements.txt

COPY worker /app/worker

ENV REDIS_HOST=redis-server
ENV REDIS_PORT=6379
ENV API_HOST=api-server
ENV API_PORT=8000

CMD ["python3", "worker/mais.py"]