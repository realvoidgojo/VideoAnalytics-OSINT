# Video Object Detection Project

This project implements object detection on video using a React frontend and a Flask backend, leveraging the YOLOv11 model. It allows users to upload a video, select a YOLOv11 model, and visualize object detection bounding boxes on the video.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10**
- **Node.js and npm**
- **Git** (for cloning the repository)

## Installation

1.  **Clone the repository:**

    ```
    git clone https://github.com/realvoidgojo/VideoAnalytics-OSINT
    cd VideoAnalytics-OSINT
    ```

2.  **Backend Setup (Flask):**

    - Create a virtual environment (recommended):

      ```
      python -m venv venv
      # Activate the virtual environment:
      # On Windows:
      venv\Scripts\activate
      # On macOS and Linux:
      source venv/bin/activate
      ```

    - Install the required Python packages:

      ```
      pip install flask flask-cors opencv-python ultralytics Pillow
      ```

    - **Download YOLOv11 Models:** Create a directory named `models` in your backend directory. Download the desired YOLOv11 models (e.g., `yolov11n.pt`, `yolov11s.pt`, etc.) from the [official YOLOv11 repository](https://github.com/ultralytics/ultralytics) or the [Ultralytics website](https://ultralytics.com/) and place them in the `models` directory.

    - **Set up the `data` directory:** Create an empty directory named `data` in your backend directory. This is where uploaded videos will be temporarily stored.

3.  **Frontend Setup (React + Vite):**

    - Navigate to the frontend directory:

      ```
      cd frontend
      ```

    - Install the required Node.js packages:

      ```
      npm install
      ```

## Configuration

- **Backend (Flask):**

  - Ensure that the paths to the YOLOv11 models in your `object_detection.py` file are correct, relative to the location of your `app.py` file. The default path is `./models/yolov11n.pt`.

- **Frontend (React):**

  - In `VideoDisplay.js`, verify that the `axios.post` URL (`http://localhost:5000/process_video`) matches the address where your Flask backend will be running.

## Running the Application

1.  **Start the Flask backend:**

    - From the backend directory, run:

      ```
      python app.py
      ```

    - Note the address the Flask app is running on (e.g., `http://127.0.0.1:5000`).

2.  **Start the React frontend:**

    - From the frontend directory, run:

      ```
      npm run dev
      ```

    - The React app should open in your browser (usually at `http://localhost:3000`).

## Usage

1.  **Upload Video:** In the React app, use the "Choose File" button to upload a video file.

2.  **Select YOLOv11 Model:** Use the dropdown menu to select the desired YOLOv11 model for object detection.

3.  **View Detections:** The video will play, and the object detection bounding boxes will be displayed on top of the video.

## Project Structure

```
video-object-detection-project/
│    app.py      # Main Flask application file
│   src/        # Directory for source code
│   ├── video_processing.py #Frame extraction and processing
│   └── object_detection.py #YOLOv11 object detection
│   clips/        # Directory for footages
│   models/     # Directory for YOLOv11 models (.pt files)
│   data/       # Directory for temporarily storing uploaded videos
│   venv/       # Python virtual environment
│   test/       # to check dependencies are working
├── frontend/       # React frontend
│   ├── src/        # React source code
│   │   └── components/
│   │       └── VideoDisplay.jsx # Main component for video display and object detection
│   ├── public/     # Static assets
│   └── node_modules/ # Node.js dependencies
├── README.md       # This file
```

## Troubleshooting

- **CORS Errors:** If you encounter Cross-Origin Resource Sharing (CORS) errors in your browser's console, make sure that you have correctly enabled CORS in your Flask app using the `flask_cors` library.

- **Model Not Found Errors:** If the YOLOv11 model cannot be found, double-check that the path to the model file in `object_detection.py` is correct and that the model file exists in the specified location.

- **Video Not Playing:** If the video is not playing in the React app, make sure that the video file is a supported format and that the `videoSource` state variable is correctly set.

<video width="720" controls>
  <source src="/assets/output.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

