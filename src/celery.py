# src/celery.py
from celery import Celery
from . import video_processing, object_detection  # Import your modules

celery_app = Celery('video_processing',
                    broker='redis://localhost:6379/0',  # Replace with your Redis URL if needed
                    backend='redis://localhost:6379/0',
                    include=['src.video_processing_tasks'])  # List of modules with Celery tasks

# Optional configuration
celery_app.conf.update(
    result_expires=3600,  # Keep task results for 1 hour
)

if __name__ == '__main__':
    celery_app.start()
