# src/renderer/camera/registry.py
from typing import Dict, Type, List

from renderer.utils.logger import logger
from renderer.camera.base import CameraPathGenerator
from renderer.camera.paths.cube import CubePathGenerator
from renderer.camera.paths.orbit import OrbitPathGenerator
from renderer.camera.paths.spiral_phi import SpiralPhiPathGenerator
from renderer.camera.paths.spiral_linear import SpiralLinearPathGenerator
from renderer.camera.paths.spiral_phased import SpiralPhasedPathGenerator
from renderer.camera.paths.pole_rotation import PoleRotationPathGenerator
# Import other generators...

class CameraPathRegistry:
    """
    Manages and retrieves camera path generators.
 
    To add a new camera path:
    1. Create a new file in `camera/paths/`
    2. Implement the `CameraPathGenerator` interface
    3. Update `CameraPathType` class
    4. Register the generator in the registry
    5. Update imports

    Methods:
        register(generator_class): Registers a new camera path generator.
        get_generator(path_type): Returns an instance of the requested generator.
        available_paths: Lists all registered camera path types.
    """

    def __init__(self):
        self._generators: Dict[str, Type[CameraPathGenerator]] = {}
    
    def register(self, generator_class: Type[CameraPathGenerator]) -> None:
        """Registers a new camera path generator."""
        generator = generator_class() # Instantiate to get name
        self._generators[generator.name] = generator_class
    
    def get_generator(self, path_type: str) -> CameraPathGenerator:
        """Retrieves a camera path generator by its name."""
        logger.debug(f"Requesting generator for path type: {path_type}")
        if path_type not in self._generators:
            raise ValueError(
                f"Unknown camera path type: {path_type}. "
                f"Available paths: {', '.join(self.available_paths)}"
            )
        return self._generators[path_type]() # Return a new instance

    @property
    def available_paths(self) -> List[str]:
        """List all registered camera path types."""
        return list(self._generators.keys())

# Initialize the registry with paths
camera_registry = CameraPathRegistry()
camera_registry.register(CubePathGenerator)
camera_registry.register(OrbitPathGenerator)
camera_registry.register(SpiralPhiPathGenerator)
camera_registry.register(PoleRotationPathGenerator)
camera_registry.register(SpiralLinearPathGenerator)
camera_registry.register(SpiralPhasedPathGenerator)
# Register new generators here...

