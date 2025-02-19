# src/renderer/lighting/setups/overhead.py
from renderer.lighting.base import BaseLightSetup
from typing import List
import bpy

class OverheadLightSetup(BaseLightSetup):
    """Overhead lighting setup with fixed positions."""
    
    @property
    def name(self) -> str:
        return "overhead"
    
    def create_lights(self) -> List[bpy.types.Object]:
        self._lights = []
        for _ in range(self.config.num_lights):
            light = self._create_light()
            light.location = (0, 0, self.config.light_height)
            light.rotation_euler = (0, 0, 0)
            self._lights.append(light)
        return self._lights

    def update_positions(self, camera_angle: float) -> None:
        """No updates needed for fixed overhead lights."""
        pass
