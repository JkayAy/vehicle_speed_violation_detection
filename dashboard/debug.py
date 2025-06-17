"""
Debug utilities for Vehicle Speed Violation Detection System dashboard.
"""
from backend.database import get_violation_records

violations = get_violation_records()
print(violations)  # Ensure this outputs a list of records
