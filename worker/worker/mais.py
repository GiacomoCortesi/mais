from subtitle import SubtitleService
import time
import redis
import os
import requests
import threading
from pathlib import Path

r = redis.Redis(host=os.getenv("REDIS_HOST", "0.0.0.0"), port=os.getenv("REDIS_PORT", "6379"), db=0)

def get_file(filename: str):
    api_host = os.getenv("API_HOST", "localhost")
    api_port = os.getenv("API_PORT", "8000")
    api_url = f'http://{api_host}:{api_port}'
    response = requests.get(f'{api_url}/file/{filename}')
    if response.status_code != 200:
        return
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def cleanup_job(job_id, delay: float=30):
    if delay and delay>0:
        time.sleep(delay)
    r.json().delete(f'job:{job_id}', '$')

def process_job(job_id):
    print(f"Processing job: {job_id}")
    queue_job = r.json().get(f'job:{job_id}')
    job = queue_job
    # job = Job(**queue_job)
    # job_filename = job_info.get('filename', '')

    # job_config = job_info.get('config', {})
    # if not job.info.filename:
    #     return
    filename = job["info"]["filename"]
    job_config = job["info"]["config"]
    get_file(filename)
    subtitle_service = SubtitleService(**job_config, hugging_face_token="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")
    r.json().set(f'job:{job_id}', 'status', 'running')
    result = subtitle_service.generate_subtitles(Path(filename))
    # result = subtitle_service.generate_subtitles_mock()
    r.json().set(f'job:{job_id}', 'status', 'completed')
    r.json().set(f'job:{job_id}', 'data', result)

def jobs_loop():
    print("Starting jobs loop")
    job_retry = 1
    failed_jobs_dict = {}
    
    while True:
        job_id = r.lpop('subtitle')
        if job_id:
            # t = threading.Thread(target=process_job, args=(job_id.decode('utf-8'),))
            # t.start()
            try:
                process_job(job_id.decode())
            except Exception as e:
                try:
                    failed_jobs_dict[job_id] += 1
                except KeyError:
                    failed_jobs_dict[job_id] = 1

                if failed_jobs_dict[job_id] < job_retry:
                    # push the job back to the queue
                    r.rpush('subtitle', job_id)
        else:
            time.sleep(0.1)

def main():
    jobs_loop()

if __name__ == '__main__':
    main()