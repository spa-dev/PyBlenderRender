"""Lighting configuration settings."""

from dataclasses import dataclass
from enum import Enum

class LightType(Enum):
    """Types of lights supported by the renderer."""
    AREA = "AREA"
    SUN = "SUN"
    POINT = "POINT"
    SPOT = "SPOT"

class LightSetup(Enum):
    """Simple light arrangement patterns."""
    RANDOM = "random"
    OVERHEAD = "overhead"

@dataclass
class LightingConfig:
    """Configuration for scene lighting.
    
    Attributes:
        num_lights: Number of lights in scene (maximum: 8)
        light_type: Type of light (AREA, SUN, POINT, or SPOT)
        light_height: Height of lights above center
        light_radius: Radius for light positioning
        light_setup: Light arrangement (RANDOM or OVERHEAD)
        light_intensity: Light strength
    """
    num_lights: int = 1
    light_type: LightType = LightType.POINT
    light_height: float = 3.0
    light_radius: float = 5.0
    light_setup: LightSetup = LightSetup.RANDOM
    light_intensity: float = 0.5
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.num_lights <= 0:
            raise ValueError("Number of lights must be positive")
        if self.num_lights > 8:
            raise ValueError("Maximum number of lights is 8")
        if self.light_height <= 0:
            raise ValueError("Light height must be positive")
        if self.light_radius <= 0:
            raise ValueError("Light radius must be positive")
        if self.light_intensity <= 0:
            raise ValueError("Light intensity must be positive")
