"""
API routes for Vehicle Speed Violation Detection System backend.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from backend.detection import process_video
from backend.database import get_violation_records, save_violation_record
from backend.config import UPLOAD_DIR

router = APIRouter()

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video file for processing.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        # Process the video
        process_video(file_path)
        return {"message": "Video uploaded and processed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@router.get("/violations/")
def get_violations(camera_id: int = None):
    """
    Retrieve all stored vehicle violation records.
    """
    try:
        records = get_violation_records(camera_id)
        return {"violations": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching violations: {str(e)}")

@router.get("/analytics/violations-by-camera/")
def violations_by_camera():
    # Return count of violations per camera
    records = get_violation_records()
    from collections import Counter
    counts = Counter(r["camera_id"] for r in records)
    return dict(counts)

@router.get("/analytics/violations-by-time/")
def violations_by_time():
    # Return count of violations by hour
    records = get_violation_records()
    from collections import Counter
    import datetime
    hours = [datetime.datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S").hour for r in records]
    counts = Counter(hours)
    return dict(counts)

@router.get("/analytics/top-violators/")
def top_violators():
    # Return license plates with most violations
    records = get_violation_records()
    from collections import Counter
    plates = [r["license_plate"] for r in records]
    counts = Counter(plates)
    return counts.most_common(10)
