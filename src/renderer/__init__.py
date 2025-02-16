# src/renderer/__init__.py
"""3D Model Renderer package for generating multi-angle views."""

# Set up centralized logging
from .utils.logger import logger  
logger.debug("Initializing PyBlenderRender package")

# Import common modules
from .model_renderer import ModelRenderer
from .config.render_config import RenderConfig, Background
from .config.lighting_config import LightingConfig, LightType, LightSetup
from .config.camera_config import CameraConfig, CameraPathType, SphereCoverage
from .config.blend_config import BlendFileConfig
from .utils.coordinates import SphericalCoordinate

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
