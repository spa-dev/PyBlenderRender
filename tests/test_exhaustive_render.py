import pytest
import datetime
import json
import os
import uuid

from itertools import product
from renderer.model_renderer import ModelRenderer
from renderer.config.render_config import (
    RenderConfig, 
    RenderEngine,
    CyclesSettings,
    EeveeSettings,
    #Background # Not tested here
)
from renderer.config.lighting_config import LightingConfig, LightType, LightSetup
from renderer.config.camera_config import CameraConfig, CameraPathType, SphereCoverage
from renderer.config.blend_config import BlendFileConfig

# Define parameter values for exhaustive testing
camera_path_types = [
    #CameraPathType.SPIRAL_PHI,
    #CameraPathType.SPIRAL_LINEAR,
    #CameraPathType.SPIRAL_PHASED,
    #CameraPathType.POLE_ROTATION,
    #CameraPathType.ORBIT,
    CameraPathType.CUBE
]

light_types = [LightType.AREA] #, LightType.SUN, LightType.POINT, LightType.SPOT]
light_setups = [LightSetup.RANDOM_DYNAMIC] #, LightSetup.RANDOM_FIXED, LightSetup.OVERHEAD]
num_lights = [2, 4]  # Testing reasonable light counts

sphere_coverages = [SphereCoverage.HALF] #, SphereCoverage.FULL]

blend_configs = [
    #BlendFileConfig(keep_lights=False, keep_materials=True, keep_world_settings=False),
    BlendFileConfig(keep_lights=True, keep_materials=True, keep_world_settings=True),
    #BlendFileConfig(keep_lights=True, keep_materials=False, keep_world_settings=True),
]

# New render engine configurations
render_configs = [
    # Cycles configurations
    {
        'engine': RenderEngine.CYCLES,
        'samples': 64,
        'device': 'GPU',
        'cycles_settings': CyclesSettings(
            use_adaptive_sampling=True,
            use_denoising=True
        )
    },
    # EEVEE configurations
    {
        'engine': RenderEngine.EEVEE,
        'samples': 64,
        'device': 'GPU',
        'eevee_settings': EeveeSettings(
            use_raytracing=True,
            use_shadows=True
        )
    }
]

@pytest.mark.slow
# Create all possible combinations of test parameters
@pytest.mark.parametrize(
    "camera_path_type, light_type, light_setup, num_lights, "
    "sphere_coverage, blend_config, render_config_params",
    list(
        product(
            camera_path_types,
            light_types,
            light_setups,
            num_lights,
            sphere_coverages,
            blend_configs,
            render_configs
        )
    ),
)
def test_render_exhaustive(
    renderer,
    test_model_path,
    output_dir,
    camera_path_type,
    light_type,
    light_setup,
    num_lights,
    sphere_coverage,
    blend_config,
    render_config_params
):
    """Test rendering with exhaustive configurations including different render engines."""

    # Generate a unique output directory for each test case
    unique_output_dir = os.path.join(output_dir, f"test_{uuid.uuid4().hex}")
    os.makedirs(unique_output_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create render config with engine-specific settings
    render_config = RenderConfig(
        resolution=128,
        **render_config_params
    )
    
    lighting_config = LightingConfig(
        num_lights=num_lights,
        light_setup=light_setup,
        light_type=light_type,
        light_intensity=1,
    )
    
    camera_config = CameraConfig(
        distance=20,
        camera_path_type=camera_path_type,
        sphere_coverage=sphere_coverage,
    )

    renderer_with_configs = ModelRenderer(
        render_config=render_config,
        lighting_config=lighting_config,
        camera_config=camera_config,
        blend_config=blend_config,
    )

    renderer_with_configs.render(test_model_path, unique_output_dir)
    stats = renderer_with_configs.get_render_stats()
    
    assert stats["successful_renders"] > 0

    # Create test summary with engine info
    summary = {
        "timestamp": timestamp,
        "test_parameters": {
            "render_engine": str(render_config.engine),
            "samples": render_config.samples,
            "device": render_config.device,
            "cycles_settings": {
                "use_adaptive_sampling": render_config.cycles_settings.use_adaptive_sampling,
                "use_denoising": render_config.cycles_settings.use_denoising
            } if render_config.engine == RenderEngine.CYCLES else None,
            "eevee_settings": {
                "use_raytracing": render_config.eevee_settings.use_raytracing,
                "use_shadows": render_config.eevee_settings.use_shadows
            } if render_config.engine == RenderEngine.EEVEE else None,
            "camera_path_type": str(camera_config.camera_path_type),
            "distance": camera_config.distance,
            "sphere_coverage": str(camera_config.sphere_coverage),
            "light_type": str(lighting_config.light_type),
            "light_setup": str(lighting_config.light_setup),
            "num_lights": lighting_config.num_lights,
            "blend_config": {
                "keep_lights": blend_config.keep_lights,
                "keep_materials": blend_config.keep_materials,
                "keep_world_settings": blend_config.keep_world_settings,
            },
        },
        "render_stats": stats,
        "output_dir": unique_output_dir,
    }

    # Save summary as JSON
    summary_path = os.path.join(unique_output_dir, "render_test_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)

    # Save summary as readable text
    summary_txt_path = os.path.join(unique_output_dir, "render_test_summary.txt")
    with open(summary_txt_path, "w") as f:
        f.write(f"Render Test Summary ({timestamp})\n")
        f.write("=" * 50 + "\n")
        f.write(f"Render Engine: {render_config.engine}\n")
        f.write(f"Samples: {render_config.samples}\n")
        f.write(f"Device: {render_config.device}\n")
        
        if render_config.engine == RenderEngine.CYCLES:
            f.write("Cycles Settings:\n")
            f.write(f"  Adaptive Sampling: {render_config.cycles_settings.use_adaptive_sampling}\n")
            f.write(f"  Denoising: {render_config.cycles_settings.use_denoising}\n")
        else:
            f.write("EEVEE Settings:\n")
            f.write(f"  Raytracing: {render_config.eevee_settings.use_raytracing}\n")
            f.write(f"  Shadows: {render_config.eevee_settings.use_shadows}\n")
            
        f.write(f"Camera Path Type: {camera_config.camera_path_type}\n")
        f.write(f"Distance: {camera_config.distance}\n")
        f.write(f"Sphere Coverage: {camera_config.sphere_coverage}\n")
        f.write(f"Light Type: {lighting_config.light_type}\n")
        f.write(f"Light Setup: {lighting_config.light_setup}\n")
        f.write(f"Number of Lights: {lighting_config.num_lights}\n")
        f.write(f"Blend Config: {blend_config}\n")
        f.write("=" * 50 + "\n")
        f.write(f"Total Renders: {stats['total_renders']}\n")
        f.write(f"Successful: {stats['successful_renders']}\n")
        f.write(f"Failed: {stats['failed_renders']}\n")
        f.write(f"Render Time: {stats['render_time']:.2f}s\n")
        f.write(f"Output Directory: {unique_output_dir}\n")