"""
YOLOv8 detection and speed calculation logic for Vehicle Speed Violation Detection System backend.
"""

# """Here is the detection.py file, which includes the logic for processing videos, detecting vehicles using YOLOv8, calculating speeds, identifying violations, and extracting license plate numbers with OCR."""

# import cv2
# import time
# from ultralytics import YOLO
# from backend.ocr import extract_license_plate
# from backend.database import save_violation_record
# from backend.config import YOLO_MODEL_PATH, DEFAULT_SPEED_LIMIT

# # Initialize YOLOv8 model
# # YOLOv8 = 'models/yolov8n.pt'
# # yolo = YOLO_MODEL_PATH
# yolo = YOLO(r'C:\Users\NOCAY\Desktop\fastapiyolo\models\best11n.pt')

# # Function to calculate speed
# def calculate_speed(prev_position, curr_position, time_diff):
#     """
#     Calculate speed based on positions across frames.
#     Speed is returned in km/h.
#     """
#     distance_pixels = ((curr_position[0] - prev_position[0]) ** 2 + (curr_position[1] - prev_position[1]) ** 2) ** 0.5
#     # Convert distance in pixels to meters (use scaling factor based on camera setup)
#     scaling_factor = 0.05  
#     distance_meters = distance_pixels * scaling_factor
#     speed_mps = distance_meters / time_diff  # Speed in meters per second
#     speed_kmph = speed_mps * 3.6  # Convert to km/h
#     return speed_kmph

# def process_video(file_path):
#     """
#     Process the video to detect vehicles, calculate speeds, and identify violations.
#     """
#     try:
#         # Open the video file
#         cap = cv2.VideoCapture(file_path)
#         if not cap.isOpened():
#             raise ValueError(f"Unable to open video file: {file_path}")

#         # Variables to track previous positions and timestamps
#         vehicle_positions = {}
#         frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
#         time_interval = 1 / frame_rate

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             # Run YOLOv8 detection
#             detections = yolo.detect(frame)

#             for det in detections:
#                 if det["label"] == "car" or det["label"] == "truck":  # Detect vehicles
#                     vehicle_id = det["id"]
#                     bbox = det["bbox"]
#                     center_x = (bbox[0] + bbox[2]) // 2
#                     center_y = (bbox[1] + bbox[3]) // 2
#                     curr_position = (center_x, center_y)

#                     # Check for previous position to calculate speed
#                     if vehicle_id in vehicle_positions:
#                         prev_position, prev_time = vehicle_positions[vehicle_id]
#                         curr_time = time.time()
#                         speed = calculate_speed(prev_position, curr_position, curr_time - prev_time)

#                         # Check for speed violations
#                         if speed > DEFAULT_SPEED_LIMIT:
#                             # Extract license plate
#                             license_plate = extract_license_plate(frame, bbox)
                            
#                             # Save violation record
#                             save_violation_record(
#                                 vehicle_type=det["label"],
#                                 license_plate=license_plate,
#                                 speed=speed,
#                                 timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
#                             )
                            
#                     # Update position and time
#                     vehicle_positions[vehicle_id] = (curr_position, time.time())

#         cap.release()
#         print(f"Processing completed for {file_path}")
#     except Exception as e:
#         print(f"Error processing video {file_path}: {e}")


import cv2
import time
from ultralytics import YOLO
from .ocr import extract_license_plate
from .database import save_violation_record
from .config import YOLO_MODEL_PATH, DEFAULT_SPEED_LIMIT, ALERT_EMAIL, ALERT_SMTP_SERVER, ALERT_SMTP_PORT, ALERT_EMAIL_USER, ALERT_EMAIL_PASS
import smtplib
from email.mime.text import MIMEText

# Initialize YOLOv8 model
yolo = YOLO(YOLO_MODEL_PATH)

# Function to calculate speed
def calculate_speed(prev_position, curr_position, time_diff):
    """
    Calculate speed based on positions across frames.
    Speed is returned in km/h.
    """
    distance_pixels = ((curr_position[0] - prev_position[0]) ** 2 + (curr_position[1] - prev_position[1]) ** 2) ** 0.5
    # Convert distance in pixels to meters (use scaling factor based on camera setup)
    scaling_factor = 0.05  
    distance_meters = distance_pixels * scaling_factor
    speed_mps = distance_meters / time_diff  # Speed in meters per second
    speed_kmph = speed_mps * 3.6  # Convert to km/h
    return speed_kmph

def process_video(file_path):
    """
    Process the video to detect vehicles, calculate speeds, and identify violations.
    """
    try:
        # Open the video file
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise ValueError(f"Unable to open video file: {file_path}")

        # Variables to track previous positions and timestamps
        vehicle_positions = {}
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        time_interval = 1 / frame_rate

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Run YOLOv8 detection
            results = yolo(frame)  # Call YOLO model
            detections = results[0].boxes  # Access bounding boxes from the first frame result

            for det in detections:
                cls = int(det.cls[0])  # Class ID
                conf = det.conf[0]  # Confidence score
                bbox = det.xyxy[0].tolist()  # Bounding box coordinates [xmin, ymin, xmax, ymax]

                # Map class IDs to vehicle types
                if cls in [2, 7]:  # Assuming 2: car, 7: truck (update based on your model classes)
                    vehicle_id = id(det)  # Use a unique identifier for this detection
                    center_x = (bbox[0] + bbox[2]) // 2
                    center_y = (bbox[1] + bbox[3]) // 2
                    curr_position = (center_x, center_y)

                    # Check for previous position to calculate speed
                    if vehicle_id in vehicle_positions:
                        prev_position, prev_time = vehicle_positions[vehicle_id]
                        curr_time = time.time()
                        speed = calculate_speed(prev_position, curr_position, curr_time - prev_time)

                        # Check for speed violations
                        if speed > DEFAULT_SPEED_LIMIT:
                            # Extract license plate
                            license_plate = extract_license_plate(frame, bbox)
                            
                            # Save violation record
                            save_violation_record(
                                vehicle_type="car" if cls == 2 else "truck",
                                license_plate=license_plate,
                                speed=speed,
                                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                            )
                            
                    # Update position and time
                    vehicle_positions[vehicle_id] = (curr_position, time.time())

        cap.release()
        print(f"Processing completed for {file_path}")
    except Exception as e:
        print(f"Error processing video {file_path}: {e}")

def process_frame(frame):
    """
    Process a single frame: detect vehicles, calculate speed, and record violations if any.
    Returns the frame with bounding boxes and labels drawn.
    """
    # Run YOLOv8 detection
    results = yolo(frame)
    detections = results[0].boxes
    current_time = time.time()
    for det in detections:
        cls = int(det.cls[0])
        conf = det.conf[0]
        bbox = det.xyxy[0].tolist()
        if cls in [2, 7]:  # Example: 2=car, 7=truck
            vehicle_id = id(det)
            center_x = (bbox[0] + bbox[2]) // 2
            center_y = (bbox[1] + bbox[3]) // 2
            curr_position = (center_x, center_y)
            # Speed calculation (store previous positions in a global dict)
            if not hasattr(process_frame, 'vehicle_positions'):
                process_frame.vehicle_positions = {}
            vehicle_positions = process_frame.vehicle_positions
            if vehicle_id in vehicle_positions:
                prev_position, prev_time = vehicle_positions[vehicle_id]
                speed = calculate_speed(prev_position, curr_position, current_time - prev_time)
                if speed > DEFAULT_SPEED_LIMIT:
                    license_plate = extract_license_plate(frame, bbox)
                    save_violation_record(
                        vehicle_type="car" if cls == 2 else "truck",
                        license_plate=license_plate,
                        speed=speed,
                        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    send_alert_email(
                        vehicle_type="car" if cls == 2 else "truck",
                        license_plate=license_plate,
                        speed=speed,
                        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    )
            vehicle_positions[vehicle_id] = (curr_position, current_time)
            # Draw bounding box and label
            x1, y1, x2, y2 = map(int, bbox)
            label = f"{'car' if cls == 2 else 'truck'}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
    return frame

def send_alert_email(vehicle_type, license_plate, speed, timestamp, camera_id=None):
    if not ALERT_EMAIL:
        return
    subject = "Speed Violation Alert"
    body = f"Vehicle: {vehicle_type}\nLicense Plate: {license_plate}\nSpeed: {speed:.2f} km/h\nTime: {timestamp}"
    if camera_id is not None:
        body += f"\nCamera: {camera_id}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = ALERT_EMAIL_USER
    msg["To"] = ALERT_EMAIL
    try:
        with smtplib.SMTP(ALERT_SMTP_SERVER, ALERT_SMTP_PORT) as server:
            server.starttls()
            server.login(ALERT_EMAIL_USER, ALERT_EMAIL_PASS)
            server.sendmail(ALERT_EMAIL_USER, ALERT_EMAIL, msg.as_string())
    except Exception as e:
        print(f"Failed to send alert email: {e}")

