"""Camera path generator for top and bottom down views with rotation."""

from typing import List

from renderer.camera.base import CameraPathGenerator
from renderer.config.camera_config import CameraConfig, SphereCoverage
from renderer.utils.coordinates import SphericalCoordinate

class PoleRotationPathGenerator(CameraPathGenerator):
    """Generates a smooth rotation near poles while ensuring visible azimuth changes."""

    @property
    def name(self) -> str:
        return "pole_rotation"
       
    def generate_positions(self, camera_config: CameraConfig) -> List[SphericalCoordinate]:
        """Generate camera positions for smooth rotation near the poles.

        The method ensures azimuth changes are visible near the poles by offsetting elevation angles.
        HALF coverage: Rotates at a fixed elevation just below 90°.
        FULL coverage: Includes an additional rotation just above -90°.

        Args:
            camera_config: Camera configuration parameters
        
        Returns:
            List[SphericalCoordinate]: List of camera positions for pole rotations.
        """
        #TODO: move frames_per_rotation to camera_config 
        frames_per_rotation = 30  # Adjust for rotation speed
        tilt_offset = 2  # Fixed offset from 90° and -90°
        radius = camera_config.distance
        roll = camera_config.roll

        positions = [
            SphericalCoordinate(radius, (i / frames_per_rotation) * 360, 90 - tilt_offset, roll)
            for i in range(frames_per_rotation)
        ]
        
        if camera_config.sphere_coverage == SphereCoverage.FULL:
            positions.extend(
                SphericalCoordinate(radius, (i / frames_per_rotation) * 360, -90 + tilt_offset, roll)
                for i in range(frames_per_rotation)
            )
        
        return positions
