# src/renderer/lighting/setups/random_dynamic.py
import math
import numpy as np
from ..base import BaseLightSetup
from typing import List
import bpy
            
class RandomDynamicLightSetup(BaseLightSetup):
    """Lights are positioned randomly around a circular path and dynamically update 
    their positions as the camera angle changes.
    
    The lights are initially placed at evenly spaced angles around the scene, and their 
    positions are adjusted in real-time to maintain relative positioning with the camera.
    """
    
    @property
    def name(self) -> str:
        return "random_dynamic"

    def create_lights(self) -> List[bpy.types.Object]:
        self._lights = []
        self._base_angles = np.linspace(0, 360, self.config.num_lights, endpoint=False)
        
        for _ in range(self.config.num_lights):
            light = self._create_light()
            self._lights.append(light)
        return self._lights

    def update_positions(self, camera_angle: float) -> None:
        """Reposition all lights based on the current camera angle.
        
        The lights move in a circular pattern around the scene, maintaining their 
        relative spacing while adjusting dynamically to align with the camera's orientation.
        """
        for light, base_angle in zip(self._lights, self._base_angles):
            angle = (base_angle + camera_angle) % 360
            x = self.config.light_radius * math.cos(math.radians(angle))
            y = self.config.light_radius * math.sin(math.radians(angle))
            light.location = (x, y, self.config.light_height)
            light.rotation_euler = (math.radians(-45), 0, math.radians(angle))



