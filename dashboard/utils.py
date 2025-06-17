"""
Utility functions for Vehicle Speed Violation Detection System dashboard.

This file includes utility functions used across the dashboard. For example, it might include functions for formatting timestamps or any data transformations required before rendering in the dashboard
"""

import pandas as pd

def format_timestamp(timestamp):
    """
    Format a timestamp to a readable string.
    """
    return pd.to_datetime(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def process_speed_data(speed_data):
    """
    Process speed data (e.g., for filtering or statistical analysis).
    """
    # Example: Filter out speeds that are unrealistic (e.g., < 0 km/h or > 200 km/h)
    return [speed for speed in speed_data if 0 <= speed <= 200]
