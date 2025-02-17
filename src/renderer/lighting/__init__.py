# src/renderer/lighting/__init__.py
#from .registry import LightingRegistry, lighting_registry
from .registry import lighting_registry
from .base import BaseLightSetup
from .setups import OverheadLightSetup, RandomDynamicLightSetup, RandomFixedLightSetup

#TODO: check all
__all__ = [
    'lighting_registry',
    'BaseLightSetup',
    'OverheadLightSetup',
    'RandomDynamicLightSetup',
    'RandomFixedLightSetup'
]
