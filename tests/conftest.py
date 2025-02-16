# tests/conftest.py
import pytest
from pathlib import Path

from renderer.model_renderer import ModelRenderer
from renderer.config.render_config import RenderConfig
from renderer.config.lighting_config import LightingConfig, LightType, LightSetup
from renderer.config.camera_config import CameraConfig, CameraPathType, SphereCoverage
from renderer.config.blend_config import BlendFileConfig

@pytest.fixture
def test_model_path():
    """Provide path to a test 3D model"""
    # Convert Path to string for Blender compatibility
    return str(Path(__file__).parent / "test_data" / "test_model.glb")

@pytest.fixture
def output_dir():
    """Provide permanent directory for render outputs"""
    # Create a permanent directory in your tests folder
    output_path = Path(__file__).parent / "test_output"
    output_path.mkdir(exist_ok=True)
    return str(output_path)  # Convert to string for Blender compatibility

#@pytest.fixture
#def output_dir(tmp_path):
#    """Provide temporary directory for render outputs"""
#    output_path = tmp_path / "render_output"
#    output_path.mkdir(exist_ok=True)
#    return str(output_path)  # Convert to string for Blender compatibility

@pytest.fixture
def renderer():
    """Provide a ModelRenderer instance with default settings."""
    return ModelRenderer()

@pytest.fixture
def configs():
    """Provide test configuration objects."""
    return {
        "render_config": RenderConfig(
            resolution=128,
            samples=128
        ),
        "lighting_config": LightingConfig(
            num_lights=1,
            light_setup=LightSetup.OVERHEAD,
            light_type=LightType.SUN,
            light_intensity=0.2, #0.01
        ),
        "camera_config": CameraConfig(
            distance=20, #1,
            camera_path_type=CameraPathType.CUBE,
            sphere_coverage=SphereCoverage.HALF
        ),
        "blend_config": BlendFileConfig(keep_materials=True)
    }
