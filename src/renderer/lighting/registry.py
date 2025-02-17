# src/renderer/lighting/registry.py
from typing import Dict, Type, List

from renderer.utils.logger import logger
from .base import BaseLightSetup
from .setups.overhead import OverheadLightSetup
from .setups.random_dynamic import RandomDynamicLightSetup
from .setups.random_fixed import RandomFixedLightSetup

class LightingRegistry:
    """
    Manages and retrieves light setup strategies.
    
    To add a new light setup:
    1. Create a new file in `lighting/setups/`
    2. Implement the `BaseLightSetup` interface
    3. Register the setup in the registry
    4. Update imports
    
    Methods:
        register(setup_class): Registers a new light setup strategy
        get_setup(setup_type): Returns an instance of the requested setup
        available_setups: Lists all registered light setup types
    """
    def __init__(self):
        self._setups: Dict[str, Type[BaseLightSetup]] = {}
    
    def register(self, setup_class: Type[BaseLightSetup]) -> None:
        """Registers a new light setup strategy."""
        setup = setup_class(None)  # Temporary instance to get name
        self._setups[setup.name] = setup_class
    
    def get_setup(self, setup_type: str) -> BaseLightSetup:
        """Retrieves a light setup strategy by its name."""
        logger.debug(f"Requesting setup for type: {setup_type}")
        if setup_type not in self._setups:
            raise ValueError(
                f"Unknown light setup type: {setup_type}. "
                f"Available setups: {', '.join(self.available_setups)}"
            )
        return self._setups[setup_type]
    
    @property
    def available_setups(self) -> List[str]:
        """List all registered light setup types."""
        return list(self._setups.keys())

# Initialize the registry with setups
lighting_registry = LightingRegistry()
lighting_registry.register(OverheadLightSetup)
lighting_registry.register(RandomDynamicLightSetup)
lighting_registry.register(RandomFixedLightSetup)
# Register new setups here...
