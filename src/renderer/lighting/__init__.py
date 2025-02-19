# src/renderer/lighting/__init__.py
from renderer.lighting.registry import lighting_registry
from renderer.lighting.base import BaseLightSetup
from renderer.lighting.setups import OverheadLightSetup, RandomDynamicLightSetup, RandomFixedLightSetup

__all__ = [
    'lighting_registry',
    'BaseLightSetup',
    'OverheadLightSetup',
    'RandomDynamicLightSetup',
    'RandomFixedLightSetup'
]
