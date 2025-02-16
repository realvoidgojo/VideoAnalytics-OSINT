import cv2

def extract_frames_batch(video_path, interval=1, batch_size=5):
    """Extracts frames from a video at a specified interval into batches."""
    frames = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Extract frames in batches
    for start_frame in range(0, frame_count, interval * batch_size):
        batch = []
        for i in range(batch_size):
            frame_index = start_frame + i * interval
            if frame_index >= frame_count:
                break  # Ensure not exceeding the total frame count
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = cap.read()
            if not ret:
                break
            batch.append(frame)
        if batch:
            frames.append(batch)
    cap.release()
    return frames


def preprocess_frame(frame, resize_width=640, resize_height=480):
    """Resizes a frame for faster processing."""
    resized_frame = cv2.resize(frame, (resize_width, resize_height))
    return resized_frame

