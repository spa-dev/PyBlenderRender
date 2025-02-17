# src/renderer/config/camera_config.py
"""Camera configuration settings."""

from dataclasses import dataclass
from enum import Enum

class SphereCoverage(Enum):
    """Render all angles or top half of the model only."""
    HALF = "half"
    FULL = "full"

class CameraPathType(Enum):
    """Types of camera paths for rendering.
    
    Attributes:
        SPIRAL_PHI: Evenly distributed points using golden ratio
        SPIRAL_LINEAR: Linear interpolated spiral path
        SPIRAL_PHASED: Controlled rotation with distinct phases
        POLE_ROTATION: Focused rotation near poles
        CUBE: Six standard orthographic views
        ORBIT: Simple horizontal orbit
    """
    SPIRAL_PHI = "spiral_phi"
    SPIRAL_LINEAR = "spiral_lin"
    SPIRAL_PHASED = "spiral_phased"
    POLE_ROTATION = "pole_rotation"
    CUBE = "cube"
    ORBIT = "orbit"

@dataclass
class CameraConfig:
    """Configuration for camera settings and path generation.
    
    Attributes:
        distance: Camera distance from center
        min_elevation: Minimum vertical angle
        max_elevation: Maximum vertical angle
        roll: Camera roll angle
        camera_path_type: Type of camera path to generate
        camera_density: Number of total images for phi spiral or orbit
        angular_step: Base angular step for linear and phased spiral
        sphere_coverage: Camera coverage (FULL or HALF) of model

    Notes
    -----
    - If SphereCoverage.HALF is specified, camera_density will be half
      that expected.    
    """
    distance: float = 1.0
    min_elevation: float = -90.0
    max_elevation: float = 90.0
    roll: float = 0.0
    
    # Path generation parameters
    camera_path_type: CameraPathType = CameraPathType.CUBE # default
    camera_density: int = 35
    angular_step: float = 45.0
    sphere_coverage: SphereCoverage = SphereCoverage.FULL
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.distance <= 0:
            raise ValueError("Camera distance must be positive")
        
        if not -90 <= self.min_elevation <= 90:
            raise ValueError("Minimum elevation must be between -90 and 90 degrees")
        if not -90 <= self.max_elevation <= 90:
            raise ValueError("Maximum elevation must be between -90 and 90 degrees")
        if self.min_elevation > self.max_elevation:
            raise ValueError("Minimum elevation must be less than maximum elevation")
            
        if not -180 <= self.roll <= 180:
            raise ValueError("Camera roll must be between -180 and 180 degrees")
            
        if self.camera_density <= 0:
            raise ValueError("Camera density must be positive")
        if self.angular_step <= 0:
            raise ValueError("Angular step must be positive")

