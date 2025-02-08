import cv2
from src import video_processing, object_detection, face_recognition, alert_system
import asyncio
import websockets

async def send_alert(message):
    """Sends an alert to the WebSocket server."""
    uri = "ws://localhost:8765"  # Replace with your server URI if needed
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
            response = await websocket.recv()  # Wait for acknowledgement
            print(f"Alert server response: {response}")  # Log the server response
    except Exception as e:
        print(f"Websocket Error: {e}")

def blur_face(frame, x, y, w, h):
    """Blurs a face in a given frame."""
    face_roi = frame[y:y+h, x:x+w]
    blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
    frame[y:y+h, x:x+w] = blurred_face
    return frame

def main(video_path="data/test_video.mp4"):
    """Main function to process video, detect objects/faces, trigger alerts, and blur faces."""

    frames = video_processing.extract_frames(video_path, interval=30)

    for frame_num, frame in enumerate(frames):  #Enumerate the frames for proper frame display
        preprocessed_frame = video_processing.preprocess_frame(frame)

        # Object Detection
        object_results = object_detection.detect_objects(preprocessed_frame)
        print(f"Frame {frame_num}: Object Detection Results:", object_results)

        # Face Recognition (Commented out unless you have a database)
        #face_results = face_recognition.recognize_faces(preprocessed_frame)
        #print(f"Frame {frame_num}: Face Recognition Results:", face_results)

        # Simple Alert Example (Detecting a person)
        for obj in object_results:
            if obj and hasattr(obj, 'boxes') and obj.boxes: #check if obj and obj.boxes is not none before attempting to use
                for box in obj.boxes:
                    if obj.names[int(box.cls[0])] == 'person': # Check if object is a person
                        asyncio.run(send_alert(f"Person detected in frame {frame_num}!")) #add frame num to message

        # Face Blurring (Placeholder - requires actual face coordinates from face recognition)
        #if face_results: #check if faces are detected, you must uncomment face detection code
        #   for (x, y, w, h) in faces: #Need to populate faces from face recognition.
        #        preprocessed_frame = blur_face(preprocessed_frame, x, y, w, h)

        # Display the frame (optional, requires a GUI)
        cv2.imshow("Processed Frame", preprocessed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
