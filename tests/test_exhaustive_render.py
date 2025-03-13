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
    # Background # Not tested here
)
from renderer.config.lighting_config import LightingConfig, LightType, LightSetup
from renderer.config.camera_config import CameraConfig, CameraPathType, SphereCoverage
from renderer.config.blend_config import BlendFileConfig

# Define parameter values for exhaustive testing
camera_path_types = [
    # CameraPathType.SPIRAL_PHI,
    # CameraPathType.SPIRAL_LINEAR,
    # CameraPathType.SPIRAL_PHASED,
    # CameraPathType.POLE_ROTATION,
    # CameraPathType.ORBIT,
    CameraPathType.CUBE
]

light_types = [LightType.AREA]  # , LightType.SUN, LightType.POINT, LightType.SPOT]
light_setups = [
    #LightSetup.RANDOM_DYNAMIC,
    #LightSetup.RANDOM_FIXED,
    LightSetup.OVERHEAD,
    LightSetup.THREE_POINT
]
num_lights = [2, 4]  # Testing reasonable light counts

sphere_coverages = [SphereCoverage.HALF]  # , SphereCoverage.FULL]

blend_configs = [
    # BlendFileConfig(keep_lights=False, keep_materials=True, keep_world_settings=False),
    BlendFileConfig(keep_lights=True, keep_materials=True, keep_world_settings=True),
    # BlendFileConfig(keep_lights=True, keep_materials=False, keep_world_settings=True),
]

# New render engine configurations
render_configs = [
    # Cycles configurations
    {
        "engine": RenderEngine.CYCLES,
        "samples": 64,
        "device": "GPU",
        "cycles_settings": CyclesSettings(
            use_adaptive_sampling=True, use_denoising=True
        ),
    },
    # EEVEE configurations
    {
        "engine": RenderEngine.EEVEE,
        "samples": 64,
        "device": "GPU",
        "eevee_settings": EeveeSettings(use_raytracing=True, use_shadows=True),
    },
]

@pytest.mark.slow
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
            render_configs,
        )
    ),
)
def test_render_exhaustive(
    # renderer_with_configs instance is created below
    test_model_path,
    output_dir,
    camera_path_type,
    light_type,
    light_setup,
    num_lights,
    sphere_coverage,
    blend_config,
    render_config_params,
):
    """Test rendering with exhaustive configurations including different render engines."""

    # Generate a unique output directory for each test case
    unique_output_dir = os.path.join(output_dir, f"test_{uuid.uuid4().hex}")
    os.makedirs(unique_output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create render config with engine-specific settings
    render_config = RenderConfig(resolution=128, **render_config_params)

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
    
    # Define custom light parameters once to use throughout
    custom_light_params = None
    if light_setup == LightSetup.THREE_POINT:
        custom_light_params = [
            {
                "color": (1.0, 0.90, 0.90),
                "cutoff_distance": 30.0,
                "use_shadow": True,
                "specular_factor": 0.8,
                "diffuse_factor": 0.9
            },
            {
                "color": (0.95, 0.95, 1.0),
                "cutoff_distance": 25.0,
                "use_shadow": True,
                "specular_factor": 0.7,
                "transmission_factor": 0.1
            },
            {
                "color": (0.90, 0.90, 1.0),
                "cutoff_distance": 20.0,
                "use_shadow": False,
                "contact_shadow_distance": 0.2,
                "contact_shadow_bias": 0.02
            },
        ]
        
        # Try to access the lighting setup if it's initialized
        if hasattr(renderer_with_configs, "_lighting_setup") and renderer_with_configs._lighting_setup:
            if hasattr(renderer_with_configs._lighting_setup, "set_custom_params"):
                renderer_with_configs._lighting_setup.set_custom_params(custom_light_params)

    renderer_with_configs.render(test_model_path, unique_output_dir)
    stats = renderer_with_configs.get_render_stats()

    assert stats["successful_renders"] > 0

    # Build the test summary parameters
    test_parameters = {
        "render_engine": str(render_config.engine),
        "samples": render_config.samples,
        "device": render_config.device,
        "cycles_settings": (
            {
                "use_adaptive_sampling": render_config.cycles_settings.use_adaptive_sampling,
                "use_denoising": render_config.cycles_settings.use_denoising,
            }
            if render_config.engine == RenderEngine.CYCLES
            else None
        ),
        "eevee_settings": (
            {
                "use_raytracing": render_config.eevee_settings.use_raytracing,
                "use_shadows": render_config.eevee_settings.use_shadows,
            }
            if render_config.engine == RenderEngine.EEVEE
            else None
        ),
        "camera_path_type": str(camera_config.camera_path_type),
        "distance": camera_config.distance,
        "sphere_coverage": str(camera_config.sphere_coverage),
        "light_type": str(lighting_config.light_type),
        "light_setup": str(lighting_config.light_setup),
        "num_lights": lighting_config.num_lights, # TODO: Fix: Not accurate with LightSetup.THREE_POINT
        "blend_config": {
            "keep_lights": blend_config.keep_lights,
            "keep_materials": blend_config.keep_materials,
            "keep_world_settings": blend_config.keep_world_settings,
        },
    }
    
    # Add custom light parameters if applicable
    if custom_light_params:
        light_names = ["key_light", "fill_light", "back_light"]
        test_parameters["custom_light_params"] = {
            name: params for name, params in zip(light_names, custom_light_params)
        }

    # Create full summary
    summary = {
        "timestamp": timestamp,
        "test_parameters": test_parameters,
        "render_stats": stats,
        "output_dir": unique_output_dir,
    }

    # Save summary as JSON
    summary_path = os.path.join(unique_output_dir, "render_test_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)

    # Generate text summary lines
    summary_lines = [
        f"Render Test Summary ({timestamp})",
        "=" * 50,
        f"Render Engine: {render_config.engine}",
        f"Samples: {render_config.samples}",
        f"Device: {render_config.device}",
    ]
    
    # Add engine specific settings
    if render_config.engine == RenderEngine.CYCLES:
        summary_lines.extend([
            "Cycles Settings:",
            f"  Adaptive Sampling: {render_config.cycles_settings.use_adaptive_sampling}",
            f"  Denoising: {render_config.cycles_settings.use_denoising}",
        ])
    else:
        summary_lines.extend([
            "EEVEE Settings:",
            f"  Raytracing: {render_config.eevee_settings.use_raytracing}",
            f"  Shadows: {render_config.eevee_settings.use_shadows}",
        ])
    
    # Add camera and light settings
    summary_lines.extend([
        f"Camera Path Type: {camera_config.camera_path_type}",
        f"Distance: {camera_config.distance}",
        f"Sphere Coverage: {camera_config.sphere_coverage}",
        f"Light Type: {lighting_config.light_type}",
        f"Light Setup: {lighting_config.light_setup}",
        f"Number of Lights: {lighting_config.num_lights}",
        f"Blend Config: {blend_config}",
    ])
    
    # Add custom light parameters if applicable
    if custom_light_params:
        summary_lines.append("\nCustom Light Parameters:")
        for i, (name, params) in enumerate(zip(light_names, custom_light_params)):
            summary_lines.append(f"  {name}:")
            for param_name, param_value in params.items():
                summary_lines.append(f"    {param_name}: {param_value}")
    
    # Add render stats
    summary_lines.extend([
        "=" * 50,
        f"Total Renders: {stats['total_renders']}",
        f"Successful: {stats['successful_renders']}",
        f"Failed: {stats['failed_renders']}",
        f"Render Time: {stats['render_time']:.2f}s",
        f"Output Directory: {unique_output_dir}",
    ])
    
    # Save text summary
    summary_txt_path = os.path.join(unique_output_dir, "render_test_summary.txt")
    with open(summary_txt_path, "w") as f:
        f.write("\n".join(summary_lines))