"""
Utility functions for Vehicle Speed Violation Detection System backend.

"""
def format_speed(speed):
    """
    Format speed to 2 decimal places and append 'km/h'.
    """
    return f"{speed:.2f} km/h"

def scale_bbox(bbox, scale_factor):
    """
    Scale a bounding box by a factor (for resizing images or regions).
    """
    x1, y1, x2, y2 = bbox
    return [int(x1 * scale_factor), int(y1 * scale_factor), int(x2 * scale_factor), int(y2 * scale_factor)]
