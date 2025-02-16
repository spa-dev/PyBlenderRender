# src/renderer/utils/__init__.py
"""Utility functions and classes for the renderer package."""

from .logger import logger  
from .coordinates import SphericalCoordinate
#from .validation import validate_settings  # Not implemented here

__all__ = [
    'SphericalCoordinate',
    'logger'
]
