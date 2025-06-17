# Usage Guide

## Running Locally

1. Install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r backend/requirements.txt
   pip install -r dashboard/requirements.txt
   ```
2. Start the backend:
   ```sh
   make run-backend
   ```
3. Start the dashboard:
   ```sh
   make run-dashboard
   ```

## Running with Docker

1. Build and start services:
   ```sh
   docker-compose up --build
   ```
2. Access the backend at [http://localhost:8000](http://localhost:8000)
3. Access the dashboard at [http://localhost:8050](http://localhost:8050)

## Example API Calls

- **Upload Video:**
  ```sh
  curl -X POST "http://localhost:8000/upload_video" -F "file=@/path/to/video.mp4"
  ```
- **Get Violations:**
  ```sh
  curl -X GET "http://localhost:8000/violations"
  ```

## Dashboard Usage
- View live video feed and analytics
- Filter and search violation records
- Export data as CSV

## Tips
- Use `.env` to configure ports, database, and secrets
- Run `make lint` and `make test` before submitting changes 