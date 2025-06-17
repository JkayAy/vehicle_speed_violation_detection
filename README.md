Vehicle Speed Violation Detection System
This project is a vehicle speed violation detection system designed to process live video streams, detect vehicles, calculate speeds, and track violations. It uses YOLOv8 for vehicle detection, an OCR system for license plate recognition, and provides a dashboard to visualize detected violations. The system is containerized using Docker for easy setup and deployment on a local machine.

Project Structure
graphql
Copy code
project/
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── detection.py       # YOLOv8 detection and speed calculation logic
│   ├── ocr.py             # License plate OCR logic
│   ├── utils.py           # Helper functions
│   ├── config.py          # Configuration settings (local-only configs)
│   ├── database.py        # SQLite database setup
│   ├── routes.py          # API endpoints
│   ├── models.py          # SQLite database models
│   └── requirements.txt   # Backend dependencies
├── dashboard/
│   ├── app.py             # Dash application entry point
│   ├── live_feed.py       # Component for video stream
│   ├── analytics.py       # Component for analytics visualizations
│   ├── violations_table.py# Component for violations table
│   ├── assets/            # Static files (CSS, JS, etc.)
│   ├── utils.py           # Functions for interacting with the backend API
│   └── requirements.txt   # Frontend dependencies
├── data/
│   ├── uploaded_videos/   # Directory for storing uploaded videos
│   └── logs/              # Logs for debugging
├── tests/
│   ├── test_detection.py  # Unit tests for YOLOv8 module
│   ├── test_ocr.py        # Unit tests for OCR module
│   ├── test_routes.py     # Unit tests for FastAPI endpoints
│   └── test_dashboard.py  # Unit tests for Dash frontend
├── README.md              # Instructions for running the application
└── run.sh                 # Script to start both FastAPI and Dash locally
Features
Vehicle Detection: Detects vehicles in live video streams using YOLOv8.
Speed Calculation: Computes vehicle speeds based on their positions across frames.
Violation Detection: Identifies speed violations by comparing vehicle speeds with a predefined speed limit.
OCR Integration: Extracts license plate numbers from detected vehicles using an OCR system.
Interactive Dashboard: Displays live video, violations table, and analytics visualizations using Dash.
Real-time Performance: Optimized for real-time detection and scalability.
SQLite Database: Stores violation records, including license plate numbers, speeds, and timestamps.
Prerequisites
Docker: Ensure that Docker is installed and running on your machine.
Docker Compose: Required for managing multi-container applications.
Python 3.8+ (if running outside Docker).
Setup and Running Locally
1. Clone the Repository
Clone this repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/vehicle-speed-violation-detection.git
cd vehicle-speed-violation-detection
2. Build Docker Containers
Make sure Docker and Docker Compose are installed. Then, build the containers:

bash
Copy code
docker-compose build
This will build the necessary images for the backend (FastAPI), frontend (Dash), and database (SQLite).

3. Start the Application
Once the containers are built, start the application by running:

bash
Copy code
docker-compose up -d
This will start the backend API, frontend Dash application, and the SQLite database in detached mode.

4. Access the Application
Once the application is running, you can access it through the following URLs:

Backend API: http://localhost:8000/
Frontend Dashboard: http://localhost:8050/
The dashboard will display live vehicle detection, violation records, and analytics.

5. Running Tests (Optional)
You can run the unit tests to verify the application:

bash
Copy code
docker-compose exec backend pytest /app/tests/
This will run tests for the YOLOv8 module, OCR module, FastAPI endpoints, and the Dash frontend.

6. Monitor Logs (Optional)
To view the logs from your Docker containers in real time, use:

bash
Copy code
docker-compose logs -f
This will stream logs from the backend, frontend, and database containers.

API Endpoints
The FastAPI backend exposes the following key API endpoints:

POST /upload_video: Upload a video file for vehicle detection.

Example:
bash
Copy code
curl -X 'POST' \
  'http://localhost:8000/upload_video' \
  -F 'file=@/path/to/video.mp4'
GET /violations: Retrieve a list of violations, including license plate numbers, speeds, and timestamps.

Example:
bash
Copy code
curl -X 'GET' \
  'http://localhost:8000/violations'
GET /violations/speed: Retrieve violations that exceed a predefined speed limit.

Example:
bash
Copy code
curl -X 'GET' \
  'http://localhost:8000/violations/speed'
Dashboard
The Dash frontend displays:

Live Feed: Live video stream with bounding boxes around detected vehicles.
Violations Table: A table listing all recorded violations, with details like license plates and speeds.
Analytics: Visualizations of speed distributions, violation counts, and trends.
To view the dashboard, open your browser and go to:

Dashboard URL: http://localhost:8050/
Database
The application uses SQLite as the database to store violation records. The database is automatically initialized and populated when a video is processed. You can access the database directly if needed:

bash
Copy code
docker-compose exec db sqlite3 /app/data/database.db
Stopping the Application
To stop and remove the Docker containers, run:

bash
Copy code
docker-compose down
This will stop the containers and remove them from your local machine.

Troubleshooting
Dashboard not loading: Ensure the backend is running properly by checking logs: docker-compose logs backend.
Detection or OCR issues: Check if YOLOv8 and OCR modules are configured correctly, and ensure the video contains clear vehicles and license plates.
Container errors: View real-time logs with docker-compose logs -f to identify and resolve any issues.
License
This project is licensed under the MIT License. See the LICENSE file for more details.
