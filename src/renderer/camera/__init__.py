# src/renderer/camera/__init__.py
#from .base import CameraPathGenerator
#from .registry import CameraPathRegistry, registry

# src/renderer/camera/__init__.py
from .registry import camera_registry
from .base import CameraPathGenerator
from .paths import (
    CubePathGenerator,
    OrbitPathGenerator,
    SpiralPhiPathGenerator,
    PoleRotationPathGenerator,
    SpiralLinearPathGenerator,
    SpiralPhasedPathGenerator
)

__all__ = [
    'camera_registry',
    'CameraPathGenerator',
    'CubePathGenerator',
    'OrbitPathGenerator',
    'SpiralPhiPathGenerator',
    'PoleRotationPathGenerator',
    'SpiralLinearPathGenerator',
    'SpiralPhasedPathGenerator'
]
