"""
Database models for Vehicle Speed Violation Detection System backend.
"""

from pydantic import BaseModel
from typing import List, Optional

class ViolationRecord(BaseModel):
    id: Optional[int]
    vehicle_type: str
    license_plate: str
    speed: float
    timestamp: str

class ViolationResponse(BaseModel):
    violations: List[ViolationRecord]
