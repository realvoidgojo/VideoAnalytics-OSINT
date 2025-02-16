import cv2
import numpy as np

def extract_frames(video_path, interval=1):
    """Extracts frames from a video at a specified interval."""
    frames = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number % interval == 0:
            frames.append(frame)

        frame_number += 1

    cap.release()
    return frames

def preprocess_frame(frame, resize_width=640, resize_height=480):
    """Resizes a frame for faster processing."""
    if not isinstance(frame, np.ndarray):
        raise ValueError("Frame is not a numpy array")
    resized_frame = cv2.resize(frame, (resize_width, resize_height))
    return resized_frame

