import { useState, useRef, useEffect } from "react";
import axios from "axios";

const VideoDisplay = () => {
  const [videoSource, setVideoSource] = useState(null);
  const [detections, setDetections] = useState([]);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [originalWidth, setOriginalWidth] = useState(0);
  const [originalHeight, setOriginalHeight] = useState(0);
  const [preprocessedWidth, setPreprocessedWidth] = useState(0);
  const [preprocessedHeight, setPreprocessedHeight] = useState(0);
  const [selectedModel, setSelectedModel] = useState("yolov8n.pt");
  const [frameInterval, setFrameInterval] = useState(1);
  const [containerWidth, setContainerWidth] = useState(720);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isVideoPaused, setIsVideoPaused] = useState(false);
  const fileInputRef = useRef(null);

  const handleVideoUpload = async (event) => {
    const file = event.target.files[0];
    setVideoSource(URL.createObjectURL(file));
    setIsProcessing(true); // Start processing

    const formData = new FormData();
    formData.append("video", file);
    formData.append("model", selectedModel);
    formData.append("interval", frameInterval);

    try {
      const response = await axios.post(
        "http://localhost:5000/process_video",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setOriginalWidth(response.data.original_width);
      setOriginalHeight(response.data.original_height);
      setPreprocessedWidth(response.data.preprocessed_width);
      setPreprocessedHeight(response.data.preprocessed_height);
      setDetections(response.data.results);
    } catch (error) {
      console.error("Error processing video:", error);
      alert("Error processing video. Please check the console for details.");
    } finally {
      setIsProcessing(false); // Processing done
    }
  };
  const handleReset = () => {
    // Reset video source, detections, and other relevant states
    setVideoSource(null);
    setDetections([]);
    setOriginalWidth(0);
    setOriginalHeight(0);
    setPreprocessedWidth(0);
    setPreprocessedHeight(0);
    setIsProcessing(false);
    setIsVideoPaused(false);
    // Clear the file input
    if (fileInputRef.current) {
      fileInputRef.current.value = ""; // Clear the selected file
    }
    // If you have a video element, you might want to pause it
    if (videoRef.current) {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
    }

    // Clear the canvas
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
  };

  // Add the methods to tell the flask server what to do
  const pauseVideoProcessing = async () => {
    try {
      await axios.post("http://localhost:5000/pause_processing");
      console.log("Video processing paused on the backend.");
    } catch (error) {
      console.error("Error pausing video processing:", error);
    }
  };
  // Add the method to tell the flask server what to do

  const resumeVideoProcessing = async () => {
    try {
      await axios.post("http://localhost:5000/resume_processing");
      console.log("Video processing resumed on the backend.");
    } catch (error) {
      console.error("Error resuming video processing:", error);
    }
  };

  const handleStopResume = () => {
    const video = videoRef.current;
    if (!video) return;

    if (isVideoPaused) {
      video.play();
      resumeVideoProcessing(); // Resume video processing on the backend
    } else {
      video.pause();
      pauseVideoProcessing(); // Pause video processing on the backend
    }
    setIsVideoPaused(!isVideoPaused);
  };

  useEffect(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    const ctx = canvas.getContext("2d");

    const drawDetections = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const currentTime = video.currentTime;
      const frameIndex = Math.floor(
        currentTime * (detections.length / video.duration)
      );

      const widthScaleFactor = canvas.width / preprocessedWidth;
      const heightScaleFactor = canvas.height / preprocessedHeight;

      if (detections.length > 0 && frameIndex < detections.length) {
        const currentFrameDetections = detections[frameIndex];
        currentFrameDetections.forEach((detection) => {
          const { class_name, confidence, box, track_id } = detection;
          if (box && box.length === 4) {
            const x1 = box[0] * widthScaleFactor;
            const y1 = box[1] * heightScaleFactor;
            const x2 = box[2] * widthScaleFactor;
            const y2 = box[3] * heightScaleFactor;

            ctx.beginPath();
            ctx.rect(x1, y1, x2 - x1, y2 - y1);
            ctx.strokeStyle = "red";
            ctx.lineWidth = 2;
            ctx.stroke();

            // Draw the label
            ctx.fillStyle = "red";
            ctx.font = "14px Arial";

            // Include track_id in the label if available
            const label = track_id
              ? `${class_name} ${confidence.toFixed(2)} (ID: ${track_id})`
              : `${class_name} ${confidence.toFixed(2)}`;
            ctx.fillText(label, x1, y1 - 5);
          }
        });
      }
      requestAnimationFrame(drawDetections);
    };

    const updateCanvasSize = () => {
      if (video.videoWidth && video.videoHeight) {
        const aspectRatio = video.videoWidth / video.videoHeight;
        canvas.width = containerWidth;
        canvas.height = containerWidth / aspectRatio;
      }
    };

    video.addEventListener("loadedmetadata", updateCanvasSize);
    video.addEventListener("play", drawDetections);

    return () => {
      video.removeEventListener("loadedmetadata", updateCanvasSize);
      video.removeEventListener("play", drawDetections);
    };
  }, [
    videoSource,
    detections,
    originalWidth,
    originalHeight,
    preprocessedWidth,
    preprocessedHeight,
    selectedModel,
    containerWidth,
    isVideoPaused,
  ]);

  return (
    <div style={{ position: "relative" }}>
      <input type="file" accept="video/*" onChange={handleVideoUpload} />

      <select
        value={selectedModel}
        onChange={(e) => setSelectedModel(e.target.value)}
      >
        <option value="yolov8n.pt">YOLOv8n</option>
        <option value="yolov8s.pt">YOLOv8s</option>
        <option value="yolov8m.pt">YOLOv8m</option>
        <option value="yolov8l.pt">YOLOv8l</option>
        <option value="yolov8x.pt">YOLOv8x</option>
      </select>

      <label>
        <span style={{ fontSize: 15, marginLeft: 10, marginRight: 10 }}>
          Frames
        </span>
        <input
          type="number"
          value={frameInterval}
          onChange={(e) => setFrameInterval(parseInt(e.target.value, 10))}
          min="1" // Ensure interval is at least 1
        />
      </label>
      <label style={{ marginLeft: 10, marginRight: 10 }}>
        <span style={{ fontSize: 15, marginLeft: 10, marginRight: 10 }}>
          Container Width:
        </span>
        <input
          type="number"
          value={containerWidth}
          onChange={(e) => setContainerWidth(parseInt(e.target.value, 10))}
          min="100" // Ensure container width is at least 100px
        />
      </label>

      {/* Reset and Stop buttons */}
      <button
        onClick={handleReset}
        style={{
          padding: "8px 12px",
          fontSize: "14px",
          cursor: "pointer",
          backgroundColor: "#f44336",
          color: "white",
          border: "none",
          borderRadius: "4px",
        }}
      >
        Reset
      </button>
      <button
        onClick={handleStopResume}
        style={{
          padding: "8px 12px",
          fontSize: "14px",
          cursor: "pointer",
          backgroundColor: isVideoPaused ? "#4CAF50" : "#f44336",
          color: "white",
          border: "none",
          borderRadius: "4px",
          marginLeft: "10px",
        }}
      >
        {isVideoPaused ? "Resume" : "Stop"}
      </button>

      {videoSource && (
        <div style={{ position: "relative" }}>
          <video
            ref={videoRef}
            src={videoSource}
            controls
            style={{
              zIndex: 1,
              position: "relative",
              width: `${containerWidth}px`,
              height: "auto",
              objectFit: "contain",
            }}
          />
          <canvas
            ref={canvasRef}
            style={{
              position: "relative",
              top: 0,
              left: 0,
              zIndex: 2,
              padding: "5px",
              pointerEvents: "none",
              marginTop: "10px", // Add some space between video and canvas
            }}
          />
        </div>
      )}
    </div>
  );
};

export default VideoDisplay;
