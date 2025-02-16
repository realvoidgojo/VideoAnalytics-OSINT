# Video Analytics and Object Detection Project

This project demonstrates real-time object detection in videos using a React frontend and a Flask backend. It utilizes the YOLO model for object detection, Celery for asynchronous task management, and Redis for message brokering.

## Prerequisites

Before you begin, ensure that you have the following installed:

*   **Python 3.10+**
*   **Node.js and npm**
*   **Git** (for cloning the repository)
*   **Redis** (for Celery message broker and result backend)

    *   **Ubuntu:** `sudo apt update && sudo apt install redis-server`
    *   **macOS:** `brew install redis`

    *For Nvidia GPU (Optional - but highly recommended for performance)*

    *   **CUDA Toolkit:** Version 11.6 or higher (check compatibility with PyTorch)
    *   **cuDNN:** Version matching your CUDA Toolkit
    *   **PyTorch with CUDA support:**

## Installation

1.  **Clone the repository:**

    ```
    git clone https://github.com/realvoidgojo/VideoAnalytics-OSINT
    cd VideoAnalytics-OSINT
    ```

2.  **Backend Setup (Flask & Celery):**

    *   Create a virtual environment (recommended):

        ```
        python -m venv venv
        source venv/bin/activate  # Linux or macOS
        # OR
        venv\Scripts\activate  # Windows
        ```

    *   Install the required Python packages:

        ```
        pip install -r requirements.txt
        ```

        *If you want CUDA, follow this instructions (check CUDA compatibility)*

        ```
        pip uninstall torch torchvision torchaudio
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu116 #replace cu116 with CUDA version
        ```

    *   **Create `requirements.txt`** It is strongly recommended to regenerate this file after installation to keep it up to date.

        ```
        pip freeze > requirements.txt
        ```

    *   **Download YOLO Models:**
        Download a YOLO model (e.g., `yolov8n.pt`) from the [official YOLO repository](https://github.com/ultralytics/ultralytics) or the [Ultralytics website](https://ultralytics.com/) and place it in the `models` directory.
    *   **Set up the `data` directory:** Create an empty directory named `data` in your backend directory. This is where uploaded videos will be temporarily stored.

3.  **Frontend Setup (React + Vite):**

    *   Navigate to the frontend directory:

        ```
        cd frontend
        ```

    *   Install the required Node.js packages:

        ```
        npm install
        ```

## Configuration

*   **Backend (Flask & Celery):**

    *   Ensure that the paths to the YOLO models in your `object_detection.py` file are correct, relative to the location of your `app.py` file. The default path is `./models/yolov8n.pt`. Ensure that the models are not corrupted, or please download from Ultralytics and replace them with their respective paths and names.
    *   Configure Redis connection settings in `src/celeryconfig.py` if necessary.
    *   If running on CPU, make sure `device = "cpu"` in `object_detection.py`.
    *   If running on GPU, make sure `device = "cuda"` in `object_detection.py` and CUDA is properly configured. You can verify CUDA installation by running `nvidia-smi`.
*   **Frontend (React):**

    *   In `VideoDisplay.jsx`, verify that the Axios POST URL (`http://localhost:5000/process_video`) matches the address where your Flask backend will be running.

## Running the Application

1.  **Start Redis:**

    *   Ensure Redis server is running.

2.  **Start the Celery worker:**

    *   From the project's root directory, run:

        ```
        celery -A src.celery.celery_app worker --loglevel=info --pool=threads -c 4
        ```

        *   Adjust the `-c` option (concurrency) to match the number of CPU cores you want to use. You can try other values like `-c 8` depending on your hardware.
        *   If you get CUDA errors, it means CUDA it's not installed properly.

3.  **Start the Flask backend:**

    *   From the project's root directory, run:

        ```
        python app.py
        ```

        *   Note the address the Flask app is running on (e.g., `http://127.0.0.1:5000`).

4.  **Start the React frontend:**

    *   From the frontend directory, run:

        ```
        npm run dev
        ```

    *   The React app should open in your browser (usually at `http://localhost:3000`).

## Usage

1.  **Upload Video:** In the React app, use the "Choose File" button to upload a video file.
2.  **Select YOLO Model:** Use the dropdown menu to select the desired YOLO model for object detection.
3.  **Set Frame Interval:**  Enter the desired frame interval to skip frames for faster processing (e.g., 1 for every frame, 30 for every 30th frame).
4.  **Start Processing:** Click the "Start Processing" button. The backend will process the video in the background using Celery, and the object detections will be displayed on the video.
5.  **Monitor Task Status:** The UI will display the task ID and the processing status.
6.  **View Detections:** Once processing is complete, the video will play, and the object detection bounding boxes will be displayed on top of the video.

## Project Structure

```
video-object-detection-project/
├── app.py                   # Main Flask application file
├── src/                     # Source code directory
│   ├── celery.py              # Celery application definition
│   ├── celeryconfig.py        # Celery configuration file
│   ├── video_processing.py  # Frame extraction and preprocessing functions
│   ├── video_processing_tasks.py  # Celery tasks for video processing
│   ├── object_detection.py    # YOLO object detection functions
│   └── __init__.py            # To make directory a python package
├── models/                  # Directory for YOLO model (.pt file)
├── data/                    # Directory for temporarily storing uploaded videos
├── venv/                    # Python virtual environment
├── frontend/                # React frontend
│   ├── src/                 # React source code
│   │   ├── components/      # React components
│   │   │   └── VideoDisplay.jsx  # Main component for video display and object detection
│   ├── public/                # Static assets
│   ├── vite.config.js         # Vite configuration
│   ├── .env.example           # Example environment variables
│   ├── package.json           # Node.js dependencies
│   └── ...
├── requirements.txt         # Python dependencies
├── README.md                  # This file
└── ...
```

## Troubleshooting

*   **CORS Errors:**

    *   If you encounter Cross-Origin Resource Sharing (CORS) errors in your browser's console, ensure that you have correctly enabled CORS in your Flask app using the `flask_cors` library.
*   **Model Not Found Errors:**

    *   If the YOLO model cannot be found, double-check that the path to the model file in `object_detection.py` is correct and that the model file exists in the specified location.
*   **Video Not Playing:**

    *   If the video is not playing in the React app, make sure that the video file is a supported format and that the `videoSource` state variable is correctly set.
*   **Celery Task Errors:**

    *   Check the Celery worker logs for any errors during task execution. Common issues include missing dependencies, incorrect file paths, or CUDA initialization problems.
*   **CUDA Errors:**

    *   If you are using CUDA, ensure that your CUDA toolkit, cuDNN, and PyTorch versions are compatible. Also, verify that your NVIDIA drivers are up to date. Use `nvidia-smi` to check if CUDA is correctly recognized.
*   **"Cannot re-initialize CUDA in forked subprocess" Error:**

    *   If you encounter this error, it means you're using the `prefork` Celery pool with CUDA, which is not supported.
    *   Solution: Use the `threads` pool.
*   **Module Not Found Error with Celery:**
    *   If you have any errors when running the Celery command, this might be related to missing `__init__.py` file. Ensure that file exists at both `src` and `src/celery`

## Optimization Tips

*   **Use a GPU:** GPU acceleration significantly speeds up object detection.
*   **Adjust Frame Interval:** Increase the frame interval to skip frames and reduce the processing load.
*   **Choose a Smaller Model:** Use a smaller YOLO model (e.g., `yolov8n.pt` instead of `yolov8m.pt`) for faster inference with a slight decrease in accuracy.
*   **Increase Concurrency:** Experiment with different concurrency levels (the `-c` option in the Celery worker command) to find the optimal balance between resource utilization and task throughput.

https://github.com/user-attachments/assets/6676dffa-0451-43ef-a0bf-6a1b65836654

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.
