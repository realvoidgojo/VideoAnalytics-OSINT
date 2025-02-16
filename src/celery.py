# src/celery.py
from celery import Celery
from celery.schedules import crontab
from . import video_processing, object_detection  # Import your modules

celery_app = Celery('video_processing',
                    broker='redis://localhost:6379/0',  # Replace with your Redis URL if needed
                    backend='redis://localhost:6379/0',
                    include=['src.video_processing_tasks'])  # List of modules with Celery tasks

celery_app.config_from_object('src.celeryconfig')
# Example periodic task (optional):
# @celery_app.task
# def my_periodic_task():
#     print("This task runs every minute!")

# celery_app.conf.beat_schedule = {
#     'run-every-minute': {
#         'task': 'src.celery.my_periodic_task',
#         'schedule': crontab(minute='*/1'),
#     },
# }

if __name__ == '__main__':
    celery_app.start()
