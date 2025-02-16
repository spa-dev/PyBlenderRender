
"""Generates camera positions in two-phase spiral pattern, starting with a
full azimuthal rotation at high elevation then descending with controlled,
consistent steps."""

from typing import List

from ..base import CameraPathGenerator
from ...config.camera_config import CameraConfig, SphereCoverage
from ...utils.coordinates import SphericalCoordinate

class SpiralPhasedPathGenerator(CameraPathGenerator):
    """Generates camera positions in a spiral pattern with adaptive step sizing."""

    @property
    def name(self) -> str:
        """Return the unique name of the camera path type."""
        return "spiral_phased"    

    def generate_positions(self, camera_config: CameraConfig) -> List[SphericalCoordinate]:
        """
        Generates camera positions in a two-phase spiral pattern.

        The method begins with a full azimuthal rotation near the zenith (87° elevation) before
        transitioning into a gradual spiral descent. The descent maintains predictable step sizes
        in both azimuth and elevation, ensuring uniform coverage.

        Parameters:
            camera_config (CameraConfig): Configuration object containing:
                - distance: Camera distance from the origin.
                - roll: Camera roll angle.
                - angular_step: Base step size for azimuth calculations.

        Returns:
            List[SphericalCoordinate]: A list of spherical coordinates defining the camera positions.
        """
        coords = []
        base_step = camera_config.angular_step  # Base step for azimuth changes
        elevation_step = base_step / 2  # Smaller elevation steps for smoother descent

        # Initial conditions
        current_elevation = 85
        current_azimuth = 0

        # Determine final elevation based on sphere coverage
        final_elevation = 0 if camera_config.sphere_coverage == SphereCoverage.HALF else -85

        # Phase 1: Full rotation at the highest elevation (85°)
        while current_elevation == 85:
            coords.append(SphericalCoordinate(
                radius=camera_config.distance,
                azimuth=current_azimuth,
                elevation=current_elevation,
                roll=camera_config.roll
            ))
            current_azimuth = (current_azimuth + base_step) % 360

            # After one full rotation, start descent
            if current_azimuth == 0:
                current_elevation = 83

        # Phase 2: Spiral descent
        while current_elevation >= final_elevation:
            coords.append(SphericalCoordinate(
                radius=camera_config.distance,
                azimuth=current_azimuth,
                elevation=current_elevation,
                roll=camera_config.roll
            ))

            # Increment azimuth continuously
            current_azimuth = (current_azimuth + base_step) % 360

            # Decrease elevation only after completing a full rotation
            if current_azimuth == 0:
                current_elevation -= elevation_step

        return coords
