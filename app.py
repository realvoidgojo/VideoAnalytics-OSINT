# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from src import video_processing, object_detection
import os , shutil

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app


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
    
    model_name = request.form.get('model', 'yolov8n.pt') #if no name defaults to yolov8n
    print(f"Request for model {model_name}")

    # Save the uploaded video to a temporary location
    video_path = os.path.join('data', video_file.filename)  # Use the 'data' directory
    video_file.save(video_path)

    try:
        frames = video_processing.extract_frames(video_path)
        all_results = []
        
        for frame in frames:
            # Debug: Print frame dimensions
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
                    'class_name': detection['class'],
                    'confidence': detection['confidence'],
                    'box': detection['bbox']  # Directly use bbox
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
        if os.path.exists(video_path):
            if os.path.isdir(video_path):  # Check if it's a directory
                shutil.rmtree(video_path)  # Remove directory
            elif os.path.isfile(video_path):  # Check if it's a file  
                os.remove(video_path)

if __name__ == '__main__':
    app.run(debug=True)


