# src/renderer/lighting/setups/three_point.py
import bpy
import math
from typing import Any, Dict, List, Tuple

from renderer.lighting.base import BaseLightSetup
from renderer.utils.logger import logger
from renderer.config import LightType


class ThreePointLightSetup(BaseLightSetup):
    """
    Standard three-point studio lighting arrangement.
    - Key light: Primary light source
    - Fill light: Secondary light to reduce shadows
    - Back light: Creates separation from background
    """

    # Default positions for three-point lighting
    KEY_POSITION = (4.0762, 1.0055, 5.9039)  # Key Light
    FILL_POSITION = (-4.0, -1.0, 5.5)  # Fill Light
    BACK_POSITION = (0, 5.0, 6.5)  # Back Light

    # Default light types for each light
    DEFAULT_LIGHT_TYPES = [
        LightType.AREA,  # Key light
        LightType.AREA,  # Fill light
        LightType.AREA,  # Back light
    ]

    # Intensity factors for each light
    LIGHT_INTENSITY_FACTORS = [1.0, 0.5, 0.3]

    # Default rotations (can be overridden)
    DEFAULT_ROTATIONS = [
        (math.radians(-45), math.radians(-15), math.radians(15)),  # Key light
        (math.radians(-35), math.radians(15), math.radians(-15)),  # Fill light
        (math.radians(-60), 0, 0),  # Back light
    ]

    # Default additional parameters for each light
    DEFAULT_LIGHT_PARAMS = [
        {"color": (1.0, 0.97, 0.93)},  # Key light - slightly warm
        {"color": (0.95, 0.97, 1.0)},  # Fill light - slightly cool
        {"color": (0.98, 0.98, 1.0)},  # Back light - almost neutral
    ]

    @property
    def name(self) -> str:
        return "three_point"

    def __init__(self, config):
        super().__init__(config)
        # Initialize custom light definitions
        self.positions = [self.KEY_POSITION, self.FILL_POSITION, self.BACK_POSITION]
        self.rotations = self.DEFAULT_ROTATIONS
        self.intensity_factors = self.LIGHT_INTENSITY_FACTORS
        self.light_params = self.DEFAULT_LIGHT_PARAMS
        self.light_types = self.DEFAULT_LIGHT_TYPES

    def create_lights(self) -> List[bpy.types.Object]:
        """Create lights with custom positions and properties."""
        logger.info(
            f"User-specified num_lights: {self.config.num_lights}; "
            "creating exactly 3 lights for 3-point setup."
        )

        logger.info(
            f"User-specified light_type: {self.config.light_type}; "
            f"using predefined types {self.DEFAULT_LIGHT_TYPES} for 3-point setup."
        )

        self._lights = []

        # Create each light with its custom properties
        for i in range(min(len(self.positions), 3)):
            # Get position, rotation, and parameters
            position = self.positions[i]
            rotation = self.rotations[i] if i < len(self.rotations) else None
            intensity_factor = (
                self.intensity_factors[i] if i < len(self.intensity_factors) else 1.0
            )
            params = self.light_params[i] if i < len(self.light_params) else {}
            light_type = (
                self.light_types[i] if i < len(self.light_types) else LightType.AREA
            )

            # Create the light with all its custom properties
            light = self._create_light(
                position=position,
                rotation=rotation,
                intensity_factor=intensity_factor,
                light_type=light_type,
                **params,
            )
            self._lights.append(light)

        return self._lights

    def update_positions(self, camera_angle: float) -> None:
        """
        Update light positions based on camera angle.
        Not implemented for fixed position lights.
        """
        pass

    def set_custom_positions(self, positions: List[Tuple[float, float, float]]) -> None:
        """Set custom positions for the lights."""
        self.positions = positions

    def set_custom_rotations(self, rotations: List[Tuple[float, float, float]]) -> None:
        """Set custom rotations for the lights."""
        self.rotations = rotations

    def set_custom_intensities(self, intensity_factors: List[float]) -> None:
        """Set custom intensity factors for the lights."""
        self.intensity_factors = intensity_factors

    def set_custom_params(self, params_list: List[Dict[str, Any]]) -> None:
        """Set custom parameters for the lights."""
        self.light_params = params_list

    def set_custom_light_types(self, light_types: List[LightType]) -> None:
        """Set custom light types for the lights."""
        self.light_types = light_types
