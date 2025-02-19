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
        """Helper method to create a single light with common properties."""
        bpy.ops.object.light_add(type=self.config.light_type.value)
        light = bpy.context.active_object
        
        light.data.energy = (
            5 * self.config.light_intensity 
            if self.config.light_type == LightType.SUN
            else 1000 * self.config.light_intensity
        )
        
        if self.config.light_type == LightType.AREA:
            light.data.size = 2
            
        return light

