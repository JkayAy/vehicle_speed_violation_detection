"""
OCR module for Vehicle Speed Violation Detection System backend.

This file contains the logic for extracting license plate numbers from detected vehicles using OCR.
"""

import cv2
import numpy as np
import easyocr

# Initialize OCR reader
ocr_reader = easyocr.Reader(['en'])

def extract_license_plate(frame, bbox):
    """
    Extract license plate text from a vehicle bounding box using OCR.
    :param frame: The video frame (numpy array).
    :param bbox: The bounding box (x1, y1, x2, y2).
    :return: Extracted license plate text.
    """
    x1, y1, x2, y2 = bbox
    # Crop the region of interest (ROI)
    roi = frame[y1:y2, x1:x2]
    # Preprocess the ROI (optional: grayscale, thresholding)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Perform OCR
    results = ocr_reader.readtext(binary)
    if results:
        # Return the first detected text
        return results[0][1]
    return "UNKNOWN"
