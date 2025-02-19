# src/renderer/camera/__init__.py
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
