from renderer.config import (
    RenderConfig, 
    LightingConfig, 
    CameraConfig, 
    BlendFileConfig
)

def test_render_config():
    """Test RenderConfig initialization and values"""
    config = RenderConfig(resolution=512, samples=64)
    assert config.resolution == 512
    assert config.samples == 64

def test_camera_config():
    """Test CameraConfig initialization and values"""
    config = CameraConfig(distance=5.0, min_elevation=0)
    assert config.distance == 5.0
    assert config.min_elevation == 0
