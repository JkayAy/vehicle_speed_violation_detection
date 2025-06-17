"""
Database setup and utility functions for Vehicle Speed Violation Detection System backend.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from backend.config import SQLITE_DB_PATH

def ensure_data_directory():
    """
    Ensure the data directory exists.
    """
    data_dir = os.path.dirname(SQLITE_DB_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def setup_database(db_path):
    """
    Create the SQLite database and violations table if they don't exist.
    """
    ensure_data_directory()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type TEXT,
            license_plate TEXT,
            speed REAL,
            timestamp TEXT,
            camera_id TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_violation_record(vehicle_type, license_plate, speed, timestamp, camera_id=None):
    """
    Save a vehicle violation record to the database.
    """
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO violations (vehicle_type, license_plate, speed, timestamp, camera_id)
        VALUES (?, ?, ?, ?, ?)
    """, (vehicle_type, license_plate, speed, timestamp, camera_id))
    conn.commit()
    conn.close()

def get_violation_records(camera_id=None):
    """
    Retrieve all vehicle violation records from the database.
    """
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    if camera_id:
        cursor.execute("SELECT * FROM violations WHERE camera_id = ?", (camera_id,))
    else:
        cursor.execute("SELECT * FROM violations")
    records = cursor.fetchall()
    conn.close()
    # Format records as dictionaries
    return [
        {"id": r[0], "vehicle_type": r[1], "license_plate": r[2], "speed": r[3], "timestamp": r[4], "camera_id": r[5]}
        for r in records
    ]
