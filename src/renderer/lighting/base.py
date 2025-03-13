# src/renderer/lighting/base.py
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
import bpy
from renderer.config.lighting_config import LightingConfig, LightType
from renderer.utils.logger import logger


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

    def _create_light(
        self,
        position: Optional[Tuple[float, float, float]] = None,
        rotation: Optional[Tuple[float, float, float]] = None,
        light_type: Optional[LightType] = None,
        intensity_factor: float = 1.0,
        **kwargs,
    ) -> bpy.types.Object:
        """
        Helper method to create a single light with customizable properties.

        Args:
            position: (x, y, z) coordinates for light position
            rotation: (x, y, z) euler rotation values in radians
            light_type: Override the config light type
            intensity_factor: Multiplier for the base light intensity.
            **kwargs: Additional light parameters to set on light.data
                      (e.g., color, cutoff_distance, use_shadow)

        Notes:
            - Watt values are radiant flux, NOT electrical watts.
            - Blender's default energy for all lights is 10.0.
        """
        # Use the specified light type or fall back to config
        actual_light_type = (
            light_type.value if light_type else self.config.light_type.value
        )

        bpy.ops.object.light_add(type=actual_light_type)
        light = bpy.context.active_object

        # Set position if provided
        if position is not None:
            light.location = position

        # Set rotation if provided
        if rotation is not None:
            light.rotation_euler = rotation

        # Adjust energy calculation based on real-world values
        if actual_light_type == LightType.SUN.value:
            # Approximate clear sky sunlight: 1000 W/m²
            # Use Blender's default of 10 (1000 is crazy bright):
            light.data.energy = 10 * self.config.light_intensity * intensity_factor
        elif actual_light_type == LightType.AREA.value:
            # Approximate 4W output, matching a 1500lm PAR38 floodlight
            light.data.energy = 4 * self.config.light_intensity * intensity_factor
            # Default shape: 'SQUARE'
            # Other options: 'RECTANGLE', 'DISK', 'ELLIPSE'
            # Default size: 0.25 (X and Y dimensions)
        elif actual_light_type == LightType.SPOT.value:
            # Approximate 22W output
            light.data.energy = 22 * self.config.light_intensity * intensity_factor
            # Default spot size in Blender: 0.785398 (45 degrees)
        else:  # POINT light
            # Approximate 2.9W output, matching a 1000lm standard bulb
            light.data.energy = 2.9 * self.config.light_intensity * intensity_factor

        # Apply any additional keyword arguments to light.data
        for key, value in kwargs.items():
            if hasattr(light.data, key):
                setattr(light.data, key, value)
            else:
                logger.warning(f"Ignored invalid light parameter: {key}")

        return light
