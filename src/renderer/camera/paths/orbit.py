"""Camera path generator for simple orbit around object."""

from typing import List

from renderer.camera.base import CameraPathGenerator
from renderer.config.camera_config import CameraConfig #, TODO: SphereCoverage
from renderer.utils.coordinates import SphericalCoordinate

class OrbitPathGenerator(CameraPathGenerator):
    """Generates a simple orbit around the object along the horizontal axis."""

    @property
    def name(self) -> str:
        """Return the unique name of the camera path type."""
        return "orbit"

    def generate_positions(self, camera_config: CameraConfig) -> List[SphericalCoordinate]:
        """Generates evenly spaced camera positions in a circular orbit around the object.
        The number of positions is controlled by camera_config.camera_density.
        """
        coords = []
        num_positions = camera_config.camera_density
        radius = camera_config.distance
        
        for i in range(num_positions):
            azimuth = (i / num_positions) * 360  # Evenly spaced azimuth angles
            coords.append(SphericalCoordinate(
                radius=radius,
                azimuth=azimuth,
                elevation=0,  # Fixed at horizontal level
                roll=camera_config.roll
            ))
        
        return coords
