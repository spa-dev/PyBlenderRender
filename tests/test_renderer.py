# tests/test_renderer.py
import pytest
import os
from renderer.model_renderer import ModelRenderer

def test_debug_path(test_model_path):
    """Test that the model path exists and is properly resolved"""
    print("Resolved path:", test_model_path)
    assert os.path.exists(test_model_path), f"File not found at {test_model_path}!"

@pytest.mark.slow
def test_basic_render(renderer, test_model_path, output_dir):
    """Test that basic rendering works with default settings.

    Note: This test may be slow due to high default resolution.
    Consider using low resolution and less fewer samples. 
    """
    renderer.render(test_model_path, output_dir)
    stats = renderer.get_render_stats()
    assert stats['successful_renders'] > 0

def test_render_with_configs(renderer, test_model_path, output_dir, configs):
    """Test rendering with custom configurations."""
    renderer_with_configs = ModelRenderer(**configs)
    renderer_with_configs.render(test_model_path, output_dir)
    stats = renderer_with_configs.get_render_stats()
    assert stats['successful_renders'] > 0

#def test_invalid_model_path(renderer, output_dir):
#    """Test that appropriate error is raised for an invalid model path."""
#    invalid_path = output_dir / "nonexistent_model.glb"
#    with pytest.raises(RuntimeError, match="Model file not found"):
#        renderer.render(invalid_path, output_dir)

def test_invalid_model_path(renderer, output_dir):
    """Test that appropriate error is raised for an invalid model path."""
    invalid_path = os.path.join(output_dir, "nonexistent_model.glb")
    with pytest.raises(RuntimeError, match="Model file not found"):
        renderer.render(invalid_path, output_dir)
