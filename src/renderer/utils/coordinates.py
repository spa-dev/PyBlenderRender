# src/renderer/utils/coordinates.py
from dataclasses import dataclass

@dataclass
class SphericalCoordinate:
    radius: float
    azimuth: float
    elevation: float
    roll: float = 0

