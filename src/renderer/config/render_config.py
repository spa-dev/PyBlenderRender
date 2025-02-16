"""Render configuration settings."""

from dataclasses import dataclass
from enum import Enum
from typing import Union, Tuple, List

class Background(Enum):
    """Background type for renders."""
    WHITE = "white"
    TRANSPARENT = "transparent"

@dataclass
class RenderConfig:
    """Configuration for render settings.
    
    Attributes:
        resolution: Output resolution in pixels. A single integer 
            for square image or tuple/list for (width,height).
        samples: Number of render samples
        device: Render device ("GPU" or "CPU")
        use_denoising: Whether to use denoising
        background: Background type (WHITE or TRANSPARENT)
    """
    resolution: Union[int, Tuple[int, int], List[int]] = 1024
    samples: int = 128
    device: str = "GPU"
    use_denoising: bool = True
    background: Background = Background.WHITE
    # quiet: bool = True #  TO DO. Implemented elsewhere by default
          
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

    @property
    def resolution_x(self) -> int:
        """Get the x-resolution."""
        return self.resolution[0] if isinstance(self.resolution, (list, tuple)) else self.resolution

    @property
    def resolution_y(self) -> int:
        """Get the y-resolution."""
        return self.resolution[1] if isinstance(self.resolution, (list, tuple)) else self.resolution

