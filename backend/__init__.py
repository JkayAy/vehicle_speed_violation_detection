"""
Backend package for Vehicle Speed Violation Detection System.
"""

from . import config
from . import database
from . import detection
from . import routes
from . import ocr
from . import models
from . import utils
from . import live_detection

__all__ = [
    'config',
    'database',
    'detection',
    'routes',
    'ocr',
    'models',
    'utils',
    'live_detection'
]
