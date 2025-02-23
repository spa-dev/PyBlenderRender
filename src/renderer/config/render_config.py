"""Render configuration settings."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Union, Tuple, List, Optional

class Background(Enum):
    """Background type for renders."""
    WHITE = "white"
    TRANSPARENT = "transparent"

class RenderEngine(Enum):
    """Supported render engines."""
    CYCLES = "CYCLES"
    EEVEE = "BLENDER_EEVEE_NEXT" # bpy v<4.1 uses "BLENDER_EEVEE"

@dataclass
class CyclesSettings:
    """Configuration specific to Cycles render engine."""
    use_adaptive_sampling: bool = True
    use_denoising: bool = True

@dataclass
class EeveeSettings:
    """Configuration specific to EEVEE render engine."""
    # Applicable to BLENDER_EEVEE_NEXT
    use_raytracing: bool = True
    use_shadows: bool = False

@dataclass
class RenderConfig:
    """Configuration for render settings.
    
    Attributes:
        resolution: Output resolution in pixels. A single integer 
            for square image or tuple/list for (width,height).
        samples: Number of render samples
        engine: Render engine (CYCLES or EEVEE)
        device: Render device ("GPU" or "CPU")
        use_denoising: Whether to use denoising
        background: Background type (WHITE or TRANSPARENT)
        cycles_settings: Optional settings specific to Cycles engine
        eevee_settings: Optional settings specific to EEVEE engine
    """
    resolution: Union[int, Tuple[int, int], List[int]] = 1024
    samples: int = 128
    engine: RenderEngine = RenderEngine.CYCLES
    device: str = "GPU"
    use_denoising: bool = True
    background: Background = Background.WHITE
    cycles_settings: Optional[CyclesSettings] = None
    eevee_settings: Optional[EeveeSettings] = None
    # quiet: bool = True #  TODO. Implemented elsewhere by default
          
    def __post_init__(self):
        """Validate configuration after initialization."""
        # Handle resolution as either int or tuple/list
        if isinstance(self.resolution, (list, tuple)):
            if len(self.resolution) != 2:
                raise ValueError("Resolution must be a tuple/list of exactly two elements")
            if not all(isinstance(r, int) and r > 0 for r in self.resolution):
                raise ValueError("Resolution elements must be positive integers")
        elif isinstance(self.resolution, int):
            if self.resolution <= 0:
                raise ValueError("Resolution must be a positive integer")
        else:
            raise TypeError("Resolution must be a positive integer or a tuple/list of two positive integers")

        if self.samples <= 0:
            raise ValueError("Samples must be positive")

        if self.device not in {"GPU", "CPU"}:
            raise ValueError("Device must be either 'GPU' or 'CPU'")
        
        # Initialize engine-specific settings if not provided
        if self.cycles_settings is None:
            self.cycles_settings = CyclesSettings()
        if self.eevee_settings is None:
            self.eevee_settings = EeveeSettings()
       
    @property
    def resolution_x(self) -> int:
        """Get the x-resolution."""
        return self.resolution[0] if isinstance(self.resolution, (list, tuple)) else self.resolution

    @property
    def resolution_y(self) -> int:
        """Get the y-resolution."""
        return self.resolution[1] if isinstance(self.resolution, (list, tuple)) else self.resolution

