"""
Unit tests for FastAPI routes in Vehicle Speed Violation Detection System.

This file tests the FastAPI routes to ensure that the endpoints are functioning as expected. This would involve testing the API for uploading video frames, retrieving violation records, and handling detection requests.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_video():
    # Simulate a video upload request (use a sample video or image file)
    with open("tests/sample_video.mp4", "rb") as video_file:
        response = client.post("/upload_video", files={"file": video_file})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "detection" in response.json(), "Response should contain detection results"

def test_get_violation_records():
    # Test retrieving violation records from the database
    response = client.get("/violations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "Violation records should be a list"
    assert len(data) > 0, "There should be at least one violation record"

def test_speed_violation():
    # Test detection of speed violations via the API
    response = client.get("/violations/speed?limit=80")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "Violation records should be a list"
    assert all(record['speed'] > 80 for record in data), "All violations should have speed > 80"
