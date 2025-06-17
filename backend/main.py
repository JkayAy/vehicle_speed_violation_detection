"""
Main FastAPI application for vehicle detection, video uploads, and violation records.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from detection import process_video  # Changed to relative import
from database import setup_database, get_violation_records, save_violation_record  # Changed to relative import
from config import SQLITE_DB_PATH  # Changed to relative import
import os
import shutil
import logging

# Initialize FastAPI app
app = FastAPI(title="Vehicle Speed Violation Detection API", version="1.0")

# CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure database is set up
setup_database(SQLITE_DB_PATH)

# Directory to save uploaded videos
UPLOAD_DIR = "data/uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-video/")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Endpoint to upload a video for processing.
    """
    try:
        # Save the uploaded video to the UPLOAD_DIR
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Start processing the video in the background
        background_tasks.add_task(process_video, file_path)
        return JSONResponse({"message": "Video uploaded and processing started."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading video: {e}")

@app.get("/violations/")
async def get_violations():
    """
    Endpoint to retrieve all recorded violations.
    """
    try:
        violations = get_violation_records()
        return JSONResponse(violations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving violations: {e}")

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Vehicle Speed Violation Detection API is running."}
