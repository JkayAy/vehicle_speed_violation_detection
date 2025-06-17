"""
Configuration file for application settings, including paths and default parameters.

"""
from dotenv import load_dotenv
import os
import json

load_dotenv()

# YOLO model configuration
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "backend/yolov8n.pt")

# Database configuration
# SQLITE_DB_PATH = "data/violations.db"
SQLITE_DB_PATH = "data/database.db"


# Default speed limit (in km/h)
DEFAULT_SPEED_LIMIT = int(os.getenv("DEFAULT_SPEED_LIMIT", 60))


# Directory to save uploaded videos
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploaded_videos/")

# # Logging configuration
# LOG_FILE = "logs/app.log"

# Multi-camera support: comma-separated list or JSON
CAMERA_SOURCES = os.getenv("CAMERA_SOURCES", "0")  # e.g., "0,rtsp://ip1,rtsp://ip2"
CAMERA_SOURCES = json.loads(CAMERA_SOURCES) if CAMERA_SOURCES.strip().startswith("[") else CAMERA_SOURCES.split(",")

# Alerting config
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "")
ALERT_SMTP_SERVER = os.getenv("ALERT_SMTP_SERVER", "smtp.example.com")
ALERT_SMTP_PORT = int(os.getenv("ALERT_SMTP_PORT", 587))
ALERT_EMAIL_USER = os.getenv("ALERT_EMAIL_USER", "")
ALERT_EMAIL_PASS = os.getenv("ALERT_EMAIL_PASS", "")
