import cv2
from ultralytics import YOLO
import numpy as np
from collections import defaultdict
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

# Simple Unique ID generator (replace with more robust method if needed)
class UniqueIDGenerator:
    def __init__(self):
        self.next_id = 0

    def get_next(self):
        self.next_id += 1
        return self.next_id

def detect_objects(frames, model_path="./models/yolov8n.pt", confidence_threshold=0.5, iou_threshold=0.5):
    model = YOLO(model_path).to(device)  # Move model to GPU
    # Check if the input is a single frame or a batch of frames
    if isinstance(frames, list):
        results = model(frames, stream=False, persist=True, conf=confidence_threshold, iou=iou_threshold)  # Pass the list of frames to the model
        all_detections = []
        # Iterate over each frame's results
        for frame_result in results:
            detections = []
            if frame_result and frame_result.boxes:
                for box in frame_result.boxes:
                    conf = box.conf[0].item()
                    class_id = int(box.cls[0].item())
                    class_name = frame_result.names[class_id]
                    # Get the bounding box coordinates
                    bbox = box.xyxy[0].tolist()
                    # Get the tracking ID, if available
                    track_id = int(box.id[0].item()) if box.id is not None else None
                    detections.append({
                        'class_name': class_name,
                        'confidence': conf,
                        'box': bbox,
                        'track_id': track_id
                    })
            all_detections.append(detections)
        return all_detections  # Return a list of detections for each frame in the batch
    else:
        results = model.track(frames, persist=True, conf=confidence_threshold, iou=iou_threshold)
        detections = []
        if results and results[0].boxes:
            for box in results[0].boxes:
                conf = box.conf[0].item()
                class_id = int(box.cls[0].item())
                class_name = results[0].names[class_id]
                # Get the bounding box coordinates
                bbox = box.xyxy[0].tolist()
                # Get the tracking ID, if available
                track_id = int(box.id[0].item()) if box.id is not None else None
                detections.append({
                    'class_name': class_name,
                    'confidence': conf,
                    'box': bbox,
                    'track_id': track_id
                })
        return detections

def calculate_area(bbox):
    return abs((bbox[2] - bbox[0]) * (bbox[3] - bbox[1]))