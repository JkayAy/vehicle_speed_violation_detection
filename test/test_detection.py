"""
Unit tests for YOLOv8 detection module in Vehicle Speed Violation Detection System.

This file will contain tests for your detection module, including vehicle detection and speed calculation. It tests the functions in detection.py to ensure the vehicle detection and speed violation calculation works as expected.
"""

import pytest
import cv2
from app.detection import detect_vehicles, calculate_speed, extract_license_plate
from unittest.mock import MagicMock

@pytest.fixture
def mock_video_frame():
    # Create a mock video frame for testing
    frame = cv2.imread('tests/sample_frame.jpg')  # Replace with an actual test image
    return frame

def test_detect_vehicles(mock_video_frame):
    # Simulate vehicle detection with a mock frame
    results = detect_vehicles(mock_video_frame)
    assert isinstance(results, list), "Detection should return a list"
    assert len(results) > 0, "At least one vehicle should be detected"

def test_calculate_speed():
    # Test speed calculation between two frames
    prev_position = (100, 100)
    curr_position = (200, 200)
    time_difference = 1.0  # in seconds
    speed = calculate_speed(prev_position, curr_position, time_difference)
    assert isinstance(speed, float), "Speed should be a float"
    assert speed > 0, "Speed should be greater than 0"

def test_extract_license_plate(mock_video_frame):
    # Test license plate extraction (you can mock OCR here if needed)
    plate_number = extract_license_plate(mock_video_frame)
    assert isinstance(plate_number, str), "License plate should be a string"
    assert len(plate_number) > 0, "License plate should not be empty"
