# src/renderer/lighting/setups/__init__.py
from renderer.lighting.setups.overhead import OverheadLightSetup
from renderer.lighting.setups.random_dynamic import RandomDynamicLightSetup
from renderer.lighting.setups.random_fixed import RandomFixedLightSetup

__all__ = ['OverheadLightSetup', 'RandomDynamicLightSetup', 'RandomFixedLightSetup']
