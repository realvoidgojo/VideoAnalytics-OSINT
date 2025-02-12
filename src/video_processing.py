import cv2

def extract_frames(video_path, interval=1):
    """Extracts frames from a video at a specified interval and releases the video capture."""
    frames = []
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval == 0:
            frames.append(frame)
        frame_count += 1
    cap.release()  # Release the video capture object!
    cv2.destroyAllWindows()  #destroy any OpenCV windows
    return frames

def preprocess_frame(frame, resize_width=640, resize_height=480):
    """Resizes a frame for faster processing."""
    resized_frame = cv2.resize(frame, (resize_width, resize_height))
    return resized_frame

