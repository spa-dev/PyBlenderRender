# src/renderer/lighting/setups/random_fixed.py
import math
import numpy as np
from ..base import BaseLightSetup
from typing import List
import bpy

class RandomFixedLightSetup(BaseLightSetup):
    """Lights randomly positioned at initialization and remain fixed."""
            
    @property
    def name(self) -> str:
        return "random_fixed"
    
    def create_lights(self) -> List[bpy.types.Object]:
        self._lights = []
        angles = np.linspace(0, 360, self.config.num_lights, endpoint=False)
        
        for angle in angles:
            light = self._create_light()
            x = self.config.light_radius * math.cos(math.radians(angle))
            y = self.config.light_radius * math.sin(math.radians(angle))
            light.location = (x, y, self.config.light_height)
            light.rotation_euler = (math.radians(-45), 0, math.radians(angle))
            self._lights.append(light)
        return self._lights

    def update_positions(self, camera_angle: float) -> None:
        """No updates needed after initial positioning."""
        pass
