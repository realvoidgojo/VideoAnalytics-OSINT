import cv2
import ultralytics
from deepface import DeepFace
import asyncio
import websockets
import numpy as np

def test_opencv():
    try:
        print("OpenCV version:", cv2.__version__)
        # Create a dummy image
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imshow("Test OpenCV", img) # This might not work without a GUI
        cv2.waitKey(1)  # Wait a short time to display the image
        cv2.destroyAllWindows()
        print("OpenCV test: PASSED")
    except Exception as e:
        print("OpenCV test: FAILED", e)

def test_yolov8():
    try:
        model = ultralytics.YOLO("yolov8n.pt")  # requires internet connection for first run
        results = model("https://ultralytics.com/images/zidane.jpg") #test image, requires internet connection
        print("YOLOv8 test: PASSED")
    except Exception as e:
        print("YOLOv8 test: FAILED", e)

def test_deepface():
    try:
        # Requires internet connection to download models on first use
        result = DeepFace.verify(img1_path="./assets/face1.jpg", img2_path="./assets/face2.jpg", model_name = 'ArcFace', detector_backend = 'retinaface')  # Using online images
        print("DeepFace test: PASSED", result)
    except Exception as e:
        print("DeepFace test: FAILED", e)

async def test_websockets():
    try:
        uri = "ws://localhost:8765"  # Replace with your WebSocket server URL if different

        async with websockets.connect(uri) as websocket:
            await websocket.send("Test Message from Client")
            response = await websocket.recv()
            print(f"WebSocket response: {response}")
        print("WebSocket test: PASSED")
    except Exception as e:
        print("WebSocket test: FAILED", e)

def test_dlib():
    try:
        import dlib
        print("dlib test: PASSED")
    except Exception as e:
        print("dlib test: FAILED", e)
# Run the tests
test_opencv()
test_yolov8()
test_deepface()
test_dlib()

# Run the websocket test
asyncio.run(test_websockets())
