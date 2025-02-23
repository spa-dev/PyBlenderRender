# tests/config/test_configs.py
import pytest
from renderer.config import (
    RenderConfig,
    LightingConfig,
    CameraConfig,
    BlendFileConfig,
    RenderEngine,
    CyclesSettings,
    EeveeSettings,
    Background
)

def test_render_config_basic():
    """Test basic RenderConfig initialization and values"""
    config = RenderConfig(resolution=512, samples=64)
    assert config.resolution == 512
    assert config.samples == 64
    assert config.engine == RenderEngine.CYCLES  # Default
    assert config.device == "GPU"  # Default
    assert config.background == Background.WHITE  # Default

def test_render_config_tuple_resolution():
    """Test RenderConfig with tuple resolution"""
    config = RenderConfig(resolution=(800, 600), samples=64)
    assert config.resolution_x == 800
    assert config.resolution_y == 600

def test_render_config_cycles():
    """Test RenderConfig with Cycles settings"""
    config = RenderConfig(
        resolution=512,
        samples=64,
        engine=RenderEngine.CYCLES,
        cycles_settings=CyclesSettings(
            use_adaptive_sampling=True,
            use_denoising=False
        )
    )
    assert config.engine == RenderEngine.CYCLES
    assert config.cycles_settings.use_adaptive_sampling is True
    assert config.cycles_settings.use_denoising is False

def test_render_config_eevee():
    """Test RenderConfig with EEVEE settings"""
    config = RenderConfig(
        resolution=512,
        samples=64,
        engine=RenderEngine.EEVEE,
        eevee_settings=EeveeSettings(
            use_raytracing=True,
            use_shadows=True
        )
    )
    assert config.engine == RenderEngine.EEVEE
    assert config.eevee_settings.use_raytracing is True
    assert config.eevee_settings.use_shadows is True

def test_render_config_validation():
    """Test RenderConfig validation"""
    with pytest.raises(ValueError):
        RenderConfig(resolution=-512)  # Invalid resolution
    
    with pytest.raises(ValueError):
        RenderConfig(samples=-64)  # Invalid samples
    
    with pytest.raises(ValueError):
        RenderConfig(device="InvalidDevice")  # Invalid device
    
    with pytest.raises(ValueError):
        RenderConfig(resolution=(800,))  # Invalid resolution tuple

def test_render_config_default_settings():
    """Test RenderConfig default engine settings"""
    config = RenderConfig()
    assert config.cycles_settings is not None
    assert config.eevee_settings is not None
    assert config.cycles_settings.use_adaptive_sampling is True
    assert config.eevee_settings.use_raytracing is True

def test_camera_config():
    """Test CameraConfig initialization and values"""
    config = CameraConfig(distance=5.0, roll=90)
    assert config.distance == 5.0
    assert config.roll == 90

def test_blend_file_config():
    """Test BlendFileConfig initialization and values"""
    config = BlendFileConfig(keep_lights=True, keep_materials=False)
    assert config.keep_lights is True
    assert config.keep_materials is False

def test_lighting_config():
    """Test LightingConfig initialization and values"""
    config = LightingConfig(num_lights=2, light_intensity=0.8)
    assert config.num_lights == 2
    assert config.light_intensity == 0.8