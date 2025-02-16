"""Configuration for .blend file handling."""

from dataclasses import dataclass

@dataclass
class BlendFileConfig:
    """Configuration for .blend file settings preservation.
    
    Attributes:
        keep_lights: Whether to preserve existing lights
        keep_materials: Whether to preserve existing materials
        keep_world_settings: Whether to preserve world settings
    """
    keep_lights: bool = False
    keep_materials: bool = True
    keep_world_settings: bool = False
