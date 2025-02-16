# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
# from src import video_processing, object_detection
import os
import threading
import logging
from src.video_processing_tasks import process_video_task #Import 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Backend State Variables
processing_lock = threading.Lock()

current_video_path = None
current_frame_index = 0
frames = []  # Store extracted frames
skip_processing = False

@app.route('/process_video', methods=['POST'])
def process_video():
    """
    Processes a video file, performs object detection, and returns the results as JSON.
    """

    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'error': 'No video selected'}), 400

    model_name = request.form.get('model', 'yolov11n.pt')  # if no name defaults to yolov11n
    print(f"Request for model {model_name}")

    frame_interval = int(request.form.get('interval', 1))
    print(f"Request for frame interval {frame_interval}")

    # Save the uploaded video to a temporary location
    video_path = os.path.join('data', video_file.filename)  # Use the 'data' directory
    video_file.save(video_path)

    task = process_video_task.delay(video_path, model_name, frame_interval)
    return jsonify({'task_id': task.id, 'message': 'Processing started in background'})

@app.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    """Retrieves status of an asynchronous task."""
    task = process_video_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info,  # Can be a dictionary
        }
        if task.state == 'SUCCESS':
           response['results'] = task.info  # Add the results to the response
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

@app.route('/reset_processing', methods=['POST'])
def reset_processing():
    """Stops and resets the video processing."""
    global is_processing, is_paused, current_video_path, current_frame_index, frames, skip_processing

    with processing_lock:
        skip_processing = True  # Stop current processing
        # Ensure processing flags are reset
        is_processing = False
        is_paused = False
        current_frame_index = 0
        frames = []

    # Delete the video file
    if current_video_path and os.path.exists(current_video_path):
        try:
            os.remove(current_video_path)
            print(f"Successfully removed video file: {current_video_path} after reset.")
        except Exception as e:
            print(f"Error removing video file: {e} after reset.")
    return jsonify({'message': 'Processing will be skipped after current frame'})

# End point to pause the video
@app.route('/pause_processing', methods=['POST'])
def pause_processing():
    """Pauses the video processing."""
    global is_paused
    is_paused = True
    return jsonify({'message': 'Processing paused'})

# End point to resume the video
@app.route('/resume_processing', methods=['POST'])
def resume_processing():
    """Resumes the video processing."""
    global is_paused
    is_paused = False
    return jsonify({'message': 'Processing resumed'})

if __name__ == '__main__':
    app.run(debug=True)