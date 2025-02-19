# src/renderer/lighting/base.py
from abc import ABC, abstractmethod
from typing import List
import bpy
from renderer.config.lighting_config import LightingConfig, LightType

class BaseLightSetup(ABC):
    """Abstract base class for light arrangement strategies."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the light setup strategy."""
        pass
    
    def __init__(self, config: LightingConfig):
        self.config = config
        self._lights: List[bpy.types.Object] = []

    @abstractmethod
    def create_lights(self) -> List[bpy.types.Object]:
        """Create and return the initial light setup."""
        pass

    @abstractmethod
    def update_positions(self, camera_angle: float) -> None:
        """Update light positions based on camera angle."""
        pass

    def _create_light(self) -> bpy.types.Object:
        """
        Helper method to create a single light with realistic properties. 

        Notes:
        - Watt values are radiant flux, NOT electrical watts. 
        - Blender's default energy for all lights is 10.0.
        """
        bpy.ops.object.light_add(type=self.config.light_type.value)
        light = bpy.context.active_object

        # Adjust energy calculation based on real-world values
        if self.config.light_type == LightType.SUN:
            # Approximate clear sky sunlight: 1000 W/m²
            # Use Blender's default of 10 (1000 is crazy bright):
            light.data.energy = 10 * self.config.light_intensity

        elif self.config.light_type == LightType.AREA:
            # Approximate 4W output, matching a 1500lm PAR38 floodlight
            light.data.energy = 4 * self.config.light_intensity
            # Default shape: ‘SQUARE’ | 
            # Other options: ‘RECTANGLE’, ‘DISK’, ‘ELLIPSE’
            # Default size: 0.25 (X and Y dimensions)

        elif self.config.light_type == LightType.SPOT:
            # Approximate 22W output
            light.data.energy = 22 * self.config.light_intensity
            # Default spot size in Blender: 0.785398 (45 degrees)

        else:  # POINT light
            # Approximate 2.9W output, matching a 1000lm standard bulb
            light.data.energy = 2.9 * self.config.light_intensity

        return light

