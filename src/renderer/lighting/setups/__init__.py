# src/renderer/lighting/setups/__init__.py
from .overhead import OverheadLightSetup
from .random_dynamic import RandomDynamicLightSetup
from .random_fixed import RandomFixedLightSetup

__all__ = ['OverheadLightSetup', 'RandomDynamicLightSetup', 'RandomFixedLightSetup']
