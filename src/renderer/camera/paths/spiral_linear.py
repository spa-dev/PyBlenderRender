"""Generates camera positions in a spiral pattern of rings with adaptive step sizing."""

from typing import List

from renderer.camera.base import CameraPathGenerator
from renderer.config.camera_config import CameraConfig, SphereCoverage
from renderer.utils.coordinates import SphericalCoordinate

class SpiralLinearPathGenerator(CameraPathGenerator):
    """Generates camera positions in a spiral pattern of rings with adaptive step sizing."""

    @property
    def name(self) -> str:
        """Return the unique name of the camera path type."""
        return "spiral_lin"
    
    def generate_positions(self, camera_config: CameraConfig) -> List[SphericalCoordinate]:
        """
        Generates camera positions in a spiral pattern of rings with adaptive azimuth steps.

        Interpolates elevation linearly (elevation decreases at a constant rate).
        Adjusts azimuth step size based on elevation to ensure smooth transitions near poles. 
        The azimuth step size is reduced at higher elevations for better coverage.

        Parameters:
            camera_config (CameraConfig): Configuration object containing:
                - distance: Camera distance from the origin.
                - roll: Camera roll angle.
                - angular_step: Base step size for azimuth calculations.
                - sphere_coverage: Determines if the coverage is FULL (70° to -70°)
                or HALF (70° to 0°).

        Returns:
            List[SphericalCoordinate]: A list of spherical coordinates representing 
            the camera positions.
        
        Notes:
        - Elevation range is fixed from 70° to -70° (FULL) or 70° to 0° (HALF) to
          prevent instability near poles.
        - Azimuth steps are adaptive, with smaller steps near the poles.
        - Ensures smooth wrap-around handling for azimuth values.
        """
        coords = []
        last_azimuth = 0
        
        # Basic parameters
        max_elevation = 70 # TODO: modify to camera_config.max_elevation but with a warning
        base_angular_step = camera_config.angular_step
        
        # Number of base elevation steps (before adaptive scaling)
        if camera_config.sphere_coverage == SphereCoverage.FULL:
            elevation_range = 140  # 70° to -70°
        else:
            elevation_range = 70   # 70° to 0°
        
        num_elevation_steps = int(elevation_range / base_angular_step)
        
        # Generate points with adaptive stepping
        for i in range(num_elevation_steps + 1):
            # Calculate elevation
            t = i / num_elevation_steps
            elevation = max_elevation - (elevation_range * t)
            
            # Calculate adaptive azimuth step for this elevation
            # More points at higher elevations for smoother transitions
            elevation_factor = abs(elevation / max_elevation)  
            # scale 0.5 at max elevation, 1.0 at equator
            scale_factor = 0.5 + (0.5 * (1 - elevation_factor))  
            azimuth_step = base_angular_step * scale_factor
            
            # Calculate number of points for this elevation
            points_at_elevation = int(360 / azimuth_step)
            
            # Generate points around this elevation ring
            for j in range(points_at_elevation):
                # Calculate raw azimuth
                current_azimuth = (j * azimuth_step) % 360
                
                # Handle wrap-around for smooth transitions
                if j > 0:
                    if current_azimuth - last_azimuth > 180:
                        current_azimuth -= 360
                    elif current_azimuth - last_azimuth < -180:
                        current_azimuth += 360
                
                coords.append(SphericalCoordinate(
                    radius=camera_config.distance,
                    azimuth=current_azimuth % 360,
                    elevation=elevation,
                    roll=camera_config.roll
                ))
                
                last_azimuth = current_azimuth
        
        return coords
        
