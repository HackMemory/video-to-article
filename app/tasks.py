import time
from celery import Celery
from speech.recognizer import recognizer

from services.video_service_factory import VideoServiceFactory

celery_app = Celery("tasks", backend="redis://redis:6379/0", broker="redis://redis:6379/0")

@celery_app.task
def process_article_generation(video_url):
    service = VideoServiceFactory.create_service(video_url)
    file = service.download_video()

    data = recognizer.transcribe(file)
    print(data)
    
    return True