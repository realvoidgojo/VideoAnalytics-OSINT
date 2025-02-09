# Enhanced object_detection.py
from ultralytics import YOLO
import numpy as np

def detect_objects(frame, model_path="yolov8n.pt", confidence_threshold=0.5):
    model = YOLO(model_path)
    results = model(frame, stream=True)
    
    detections = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            conf = box.conf[0]
            cls = int(box.cls[0])
            
            if conf > confidence_threshold:
                detections.append({
                    'class': result.names[cls],
                    'confidence': float(conf),
                    'bbox': box.xyxy[0].tolist()  # Directly return bbox
                })
    
    return detections

def calculate_area(bbox):
    return abs((bbox[2] - bbox[0]) * (bbox[3] - bbox[1]))