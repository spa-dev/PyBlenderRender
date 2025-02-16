"""Camera path generator for spiral views based on the Golden ratio (phi)."""

from typing import List
import numpy as np

from ..base import CameraPathGenerator
from ...config.camera_config import CameraConfig, SphereCoverage
from ...utils.coordinates import SphericalCoordinate

class SpiralPhiPathGenerator(CameraPathGenerator):
    """Generates camera positions for spiral view (phi)."""

    @property
    def name(self) -> str:
        """Return the unique name of the camera path type."""
        return "spiral_phi"
    
    def generate_positions(self, camera_config: CameraConfig) -> List[SphericalCoordinate]:
        """Generate camera positions evenly distributed over a sphere.

        Starts from top-down view and spirals down using Golden ratio (phi)
        When SphereCoverage.HALF is specified, the bottom half is excluded.
        
        Returns:
            List[SphericalCoordinate]: List of camera positions in spherical coordinates.
        """
        
        radius = camera_config.distance
        camera_density = camera_config.camera_density
        positions = []
        
        golden_ratio = (1 + np.sqrt(5)) / 2  # For even azimuthal spacing
        indices = reversed(range(camera_density))  # Reverse order to start from the top
        
        for i in indices:
            elevation = np.degrees(np.arcsin(-1 + 2 * i / (camera_density - 1)))  # -90° to 90°
            azimuth = (360 * (i / golden_ratio)) % 360  # Spread around sphere
            
            if camera_config.sphere_coverage == SphereCoverage.HALF and elevation < 0:
                continue  # Skip bottom hemisphere for half-sphere coverage
            
            positions.append(SphericalCoordinate(radius, azimuth, elevation, 0))
        
        return positions