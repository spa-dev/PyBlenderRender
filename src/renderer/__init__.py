# src/renderer/__init__.py
"""3D Model Renderer package for generating multi-angle views."""

# Set up centralized logging
from renderer.utils.logger import logger  
logger.debug("Initializing PyBlenderRender package")

# Import common modules
from renderer.model_renderer import ModelRenderer
from renderer.config.render_config import RenderConfig, Background
from renderer.config.lighting_config import LightingConfig, LightType, LightSetup
from renderer.config.camera_config import CameraConfig, CameraPathType, SphereCoverage
from renderer.config.blend_config import BlendFileConfig
from renderer.utils.coordinates import SphericalCoordinate

__all__ = [
    'ModelRenderer',
    'RenderConfig',
    'LightingConfig',
    'CameraConfig',
    'BlendFileConfig',
    'Background',
    'SphereCoverage',
    'LightType',
    'LightSetup',
    'CameraPathType',
    'SphericalCoordinate',
    'logger'
]
