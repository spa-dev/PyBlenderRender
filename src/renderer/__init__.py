# src/renderer/__init__.py
"""3D Model Renderer package for generating multi-angle views."""

# Set up centralized logging
from renderer.utils.logger import logger  
logger.debug("Initializing PyBlenderRender package")

# Import common modules
from renderer.model_renderer import ModelRenderer
from renderer.config.blend_config import BlendFileConfig
from renderer.config.camera_config import CameraConfig, CameraPathType, SphereCoverage
from renderer.config.lighting_config import LightingConfig, LightType, LightSetup
from renderer.config.render_config import (
    RenderConfig, Background, RenderEngine, CyclesSettings, EeveeSettings
)
from renderer.utils.coordinates import SphericalCoordinate
from renderer.camera.base import CameraPathGenerator
from renderer.camera.registry import camera_registry
from renderer.camera.paths import (
    CubePathGenerator,
    OrbitPathGenerator,
    SpiralPhiPathGenerator,
    PoleRotationPathGenerator,
    SpiralLinearPathGenerator,
    SpiralPhasedPathGenerator
)
from renderer.lighting.base import BaseLightSetup
from renderer.lighting.registry import lighting_registry
from renderer.lighting.setups import (
    OverheadLightSetup, 
    RandomDynamicLightSetup, 
    RandomFixedLightSetup,
    ThreePointLightSetup
)

__all__ = [
    'ModelRenderer',
    'RenderConfig',
    'LightingConfig',
    'CameraConfig',
    'BlendFileConfig',
    'SphereCoverage',
    'LightType',
    'LightSetup',
    'CameraPathType',
    'SphericalCoordinate',
    'logger',
    # Render-related exports
    'Background',
    'RenderEngine',
    'CyclesSettings',
    'EeveeSettings',
    # Camera-related exports
    'CameraPathGenerator',
    'camera_registry',
    'CubePathGenerator',
    'OrbitPathGenerator',
    'SpiralPhiPathGenerator',
    'PoleRotationPathGenerator',
    'SpiralLinearPathGenerator',
    'SpiralPhasedPathGenerator',
    # Lighting-related exports
    'BaseLightSetup',
    'lighting_registry',
    'OverheadLightSetup',
    'RandomDynamicLightSetup',
    'RandomFixedLightSetup',
    'ThreePointLightSetup'
]

