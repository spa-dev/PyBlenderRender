"""Camera path generator for cube-style views (6 orthographic angles)."""

from typing import List

from ..base import CameraPathGenerator
from ...config.camera_config import CameraConfig, SphereCoverage
from ...utils.coordinates import SphericalCoordinate

class CubePathGenerator(CameraPathGenerator):
    """Generates camera positions for 6 standard orthographic views."""

    @property
    def name(self) -> str:
        """Return the unique name of the camera path type."""
        return "cube"
    
    def generate_positions(self, camera_config: CameraConfig) -> List[SphericalCoordinate]:
        """Generate camera positions for 6 cube faces.
        
        Creates 6 camera positions corresponding to viewing the object
        from each face of a cube (front, back, left, right, top, bottom). The camera
        positions maintain consistent orientation and distance from the object.
        
        Returns:
            List[SphericalCoordinate]: List of 6 camera positions for cube face views
        """
        # Define the 6 standard cube face views
        cube_views = [
            # Front view (0, 0, 0)
            SphericalCoordinate(
                radius=camera_config.distance,
                azimuth=0,
                elevation=0,
                roll=0
            ),
            # Right view (-90, 0, 0)
            SphericalCoordinate(
                radius=camera_config.distance,
                azimuth=90,
                elevation=0,
                roll=0
            ),
            # Back view (180, 0, 0)
            SphericalCoordinate(
                radius=camera_config.distance,
                azimuth=180,
                elevation=0,
                roll=0
            ),
            # Left view (90, 0, 0)
            SphericalCoordinate(
                radius=camera_config.distance,
                azimuth=270,
                elevation=0,
                roll=0
            ),
            # Top view (0, 90, 0)
            SphericalCoordinate(
                radius=camera_config.distance,
                azimuth=0,
                elevation=90,
                roll=0
            ),
            # Bottom view (0, -90, 0)
            SphericalCoordinate(
                radius=camera_config.distance,
                azimuth=0,
                elevation=-90,
                roll=0
            )
        ]
        
        # Filter views based on sphere coverage
        if camera_config.sphere_coverage == SphereCoverage.HALF:
            # For half coverage, exclude bottom view and any views below horizon
            cube_views = [view for view in cube_views if view.elevation >= 0]
        
        return cube_views
       
    def generate_positions_deprecated(self, camera_config: CameraConfig) -> List[SphericalCoordinate]:
        """Generate camera positions for 6 cube faces.
        
        The camera positions maintain consistent orientation and distance
        from the object for each orthographic view. When SphereCoverage.HALF
        is specified, the bottom view is excluded, returning 5 cube faces.
        
        Args:
            camera_config: Camera configuration parameters
            
        Returns:
            List of SphericalCoordinate for each cube face view
        """
        
        # Define cube face angles (azimuth, elevation)
        angles = [
            (0, 0),     # Front
            (90, 0),    # Right
            (180, 0),   # Back
            (270, 0),   # Left
            (0, 90),    # Top
            (0, -90)    # Bottom
        ]
        
        # Create camera positions
        cube_views = [
            SphericalCoordinate(camera_config.distance, az, el, 0)
            for az, el in angles
        ]
        
        # Filter views based on sphere coverage
        if camera_config.sphere_coverage == SphereCoverage.HALF:
            cube_views = [view for view in cube_views if view.elevation >= 0]
            
        return cube_views
