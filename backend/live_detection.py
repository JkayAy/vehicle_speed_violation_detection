"""
Live detection logic for Vehicle Speed Violation Detection System backend.
Supports configurable camera sources (webcam, IP camera, RTSP, etc.).
"""
import cv2
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from backend.config import CAMERA_SOURCES
from backend.detection import process_frame  # You will need to implement this

app = FastAPI()

def webcam_feed(camera_source):
    """
    Generator function to capture frames from the configured camera source and yield them as a video stream.
    """
    cap = cv2.VideoCapture(camera_source)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera source: {camera_source}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Process frame (e.g., detect vehicles)
        processed_frame = process_frame(frame)  # Implement this for YOLOv8 detection
        _, jpeg_frame = cv2.imencode('.jpg', processed_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               jpeg_frame.tobytes() + b'\r\n')
    cap.release()

@app.get("/live-feed/{camera_id}")
def live_feed(camera_id: int):
    """
    Endpoint to stream live camera feed.
    """
    if camera_id < 0 or camera_id >= len(CAMERA_SOURCES):
        raise HTTPException(status_code=404, detail="Camera not found")
    camera_source = CAMERA_SOURCES[camera_id]
    return StreamingResponse(webcam_feed(camera_source), media_type="multipart/x-mixed-replace; boundary=frame")
