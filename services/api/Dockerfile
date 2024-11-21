FROM python:3.10.12-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY openapi_server /usr/src/app/openapi_server

EXPOSE 8080

CMD ["python3", "-m", "openapi_server"]