# src/video_processing_tasks.py
from .celery import celery_app
from . import video_processing, object_detection
import os
import time
@celery_app.task(bind=True)
def process_video_task(self, video_path, model_name, frame_interval):
    """
    Processes a video file, performs object detection, and returns the results as JSON.
    """
    try:
        frames = video_processing.extract_frames(video_path, interval=frame_interval)
        all_results = []
        for i, frame in enumerate(frames):
            print(f"Processing frame {i}")
            preprocessed_frame = video_processing.preprocess_frame(frame)
            object_results = object_detection.detect_objects(preprocessed_frame, model_path=f"./models/{model_name}")
            formatted_results = []
            for detection in object_results:
                formatted_results.append({
                    'class_name': detection['class_name'],
                    'confidence': detection['confidence'],
                    'box': detection['box'],
                    'track_id': detection['track_id']
                })

            all_results.append(formatted_results)

        original_width, original_height = 720, 1280  # Simulated dimension

        return {
            'results': all_results,
            'original_width': original_width,
            'original_height': original_height,
            'preprocessed_width': 640,  # Replace with actual values
            'preprocessed_height': 480  # Replace with actual values
        }
    except Exception as e:
        print(f"Processing Error: {e}")
        return {'error': str(e)}

    finally:  # Cleanup
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
                print(f"Successfully removed video file: {video_path} after processing.")
            except Exception as e:
                print(f"Error removing video file: {e} after processing.")
