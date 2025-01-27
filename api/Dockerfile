FROM python:3.10.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./api /app/api

CMD ["fastapi", "run", "api/main.py", "--port", "8000"]