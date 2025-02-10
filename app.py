# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from src import video_processing, object_detection
import os , shutil
import threading  # Import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Backend State Variables
processing_lock = threading.Lock()
is_processing = False
is_paused = False
current_video_path = None
current_frame_index = 0
frames = []  # Store extracted frames
skip_processing = False

@app.route('/process_video', methods=['POST'])
def process_video():
    """
    Processes a video file, performs object detection, and returns the results as JSON.
    """
    global is_processing, is_paused, current_video_path, current_frame_index, frames ,  skip_processing
    
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'error': 'No video selected'}), 400
    
    model_name = request.form.get('model', 'yolov11n.pt') #if no name defaults to yolov11n
    print(f"Request for model {model_name}")

    frame_interval = int(request.form.get('interval', 1))
    print(f"Request for frame interval {frame_interval}")

    # Save the uploaded video to a temporary location
    video_path = os.path.join('data', video_file.filename)  # Use the 'data' directory
    video_file.save(video_path)

    with processing_lock:
        if is_processing:
            return jsonify({'error': 'Already processing a video'}), 400

        is_processing = True
        is_paused = False
        skip_processing = False
        current_video_path = video_path
        current_frame_index = 0
        all_results = []

    try:

        frames = video_processing.extract_frames(video_path, interval=frame_interval)
        all_results = []

        
        for i, frame in enumerate(frames):
            current_frame_index = i  # Update frame index
            # Check if processing should stop or pause
            if not is_processing or skip_processing:
                print("Processing stopped by user")
                break
            if is_paused:
                print("Processing paused by user")
                while is_paused:  # Wait while paused
                    pass  # or time.sleep(0.1) to avoid busy-waiting

            print(f"Original Frame Dimensions: {frame.shape}")

            original_height, original_width = frame.shape[:2]
            preprocessed_frame = video_processing.preprocess_frame(frame)
            
            # Debug: Print preprocessed frame dimensions
            print(f"Preprocessed Frame Dimensions: {preprocessed_frame.shape}")

            # Use updated object detection method
            object_results = object_detection.detect_objects(preprocessed_frame, model_path = f"./models/{model_name}")
            
            # Debug: Print raw object results
            print(f"Raw Object Results: {object_results}")

            formatted_results = []
            for detection in object_results:
                # Directly use detection dictionary
                formatted_results.append({
                    'class_name': detection['class_name'],
                    'confidence': detection['confidence'],
                    'box': detection['box'],  # Directly use bbox
                    'track_id': detection['track_id']
                })
            
            all_results.append(formatted_results)

        # Debug: Print total results
        print(f"Total Frames Processed: {len(all_results)}")
        print(f"Results Sample: {all_results[:2]}")

        return jsonify({
    'results': all_results,
    'original_width': original_width,
    'original_height': original_height,
    'preprocessed_width': preprocessed_frame.shape[1],  # width is shape[1]
    'preprocessed_height': preprocessed_frame.shape[0]  # height is shape[0]
})

    except Exception as e:
        print(f"Processing Error: {e}")
        return jsonify({'error': str(e)}), 500

    finally:  # Cleanup

        is_processing = False
        is_paused = False
        skip_processing = False #Reset Skip flag

        current_video_path = None
        current_frame_index = 0
        frames = []  # Clear frames

        if os.path.exists(video_path):
            if os.path.isdir(video_path):  # Check if it's a directory
                shutil.rmtree(video_path)  # Remove directory
            elif os.path.isfile(video_path):  # Check if it's a file  
                os.remove(video_path)

@app.route('/reset_processing', methods=['POST'])
def reset_processing():
    """Skips the current video processing."""
    global skip_processing
    skip_processing = True
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


