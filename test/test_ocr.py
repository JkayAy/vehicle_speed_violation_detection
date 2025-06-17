"""
Unit tests for OCR module in Vehicle Speed Violation Detection System.

This file tests the OCR (Optical Character Recognition) functionality to ensure that license plate extraction works as expected.
"""

import pytest
from app.ocr import extract_license_plate
from unittest.mock import patch

@pytest.fixture
def mock_image():
    # Simulate a test image (mocking can be used here for simplicity)
    return 'tests/sample_plate_image.jpg'  # Replace with actual image file path

def test_extract_license_plate(mock_image):
    # Test OCR extraction on a sample image
    plate_number = extract_license_plate(mock_image)
    assert isinstance(plate_number, str), "License plate should be a string"
    assert len(plate_number) > 0, "License plate should not be empty"

@patch('app.ocr.extract_license_plate')  # Mock OCR function
def test_extract_license_plate_mock(mock_extract):
    # Mock OCR result for testing
    mock_extract.return_value = "ABC1234"
    plate_number = extract_license_plate("tests/sample_plate_image.jpg")
    assert plate_number == "ABC1234", "The mocked license plate should be 'ABC1234'"
