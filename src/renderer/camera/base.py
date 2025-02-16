# src/renderer/camera/base.py
from abc import ABC, abstractmethod
from typing import List
from renderer.utils.logger import logger
from ..utils.coordinates import SphericalCoordinate

class CameraPathGenerator(ABC):
    """Abstract base class for all camera path generators."""
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of the camera path type."""
        pass
       
    @abstractmethod
    def generate_positions(self, camera_config) -> List[SphericalCoordinate]:
        """Generate a list of camera positions based on the configuration."""
        pass

