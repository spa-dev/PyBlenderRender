# If installing as a package comment out the modification to sys.path:
import sys
import os
# Ensure the src/ directory is in the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Imports
import argparse
import time
from datetime import datetime
from pathlib import Path
from renderer import *

def run_render_test(
    model_path: str,
    output_dir: str,
    render_config: RenderConfig,
    lighting_config: LightingConfig,
    camera_config: CameraConfig,
    blend_config: BlendFileConfig,
) -> dict:
    """Run a single rendering test.
    
    Args:
        model_path: Path to the 3D model file
        output_dir: Directory for output images
        render_config: Rendering configuration
        lighting_config: Lighting configuration
        camera_config: Camera configuration
        blend_config: Blender file import settings
        
    Returns:
        dict: Test results including timing and render statistics
        
    Raises:
        FileNotFoundError: If model file doesn't exist
        RuntimeError: If rendering fails
    """
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_output_dir = Path(output_dir) / timestamp
    test_output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Running render test with distance: {camera_config.distance}")
    
    # Initialize renderer with explicit configurations
    renderer = ModelRenderer(
        render_config=render_config,
        lighting_config=lighting_config,
        camera_config=camera_config,
        blend_config=blend_config
    )
    
    try:
        start_time = time.time()
        renderer.render(str(model_path), str(test_output_dir))
        stats = renderer.get_render_stats()
        
        # Log results
        logger.info("Completed render test:")
        logger.info(f"Total renders: {stats['total_renders']}")
        logger.info(f"Successful: {stats['successful_renders']}")
        logger.info(f"Failed: {stats['failed_renders']}")
        logger.info(f"Time: {stats['render_time']:.2f}s")
        
        # Create test summary
        summary = {
            'timestamp': timestamp,
            'path_type': {camera_config.camera_path_type},
            'distance': {camera_config.distance},
            'stats': stats,
            'output_dir': str(test_output_dir)
        }
        
        # Save summary to file
        summary_path = test_output_dir / 'render_test_summary.txt'
        with open(summary_path, 'w') as f:
            f.write(f"Render Test Summary ({timestamp})\n")
            f.write("=" * 50 + "\n")
            f.write(f"Path Type: {camera_config.camera_path_type}\n")
            f.write(f"Distance: {camera_config.distance}\n")
            f.write(f"Total Renders: {stats['total_renders']}\n")
            f.write(f"Successful: {stats['successful_renders']}\n")
            f.write(f"Failed: {stats['failed_renders']}\n")
            f.write(f"Time: {stats['render_time']:.2f}s\n")
        
        return summary
    
    except Exception as e:
        logger.error(f"Render test failed: {str(e)}")
        raise RuntimeError(f"Render test failed: {str(e)}") from e
    
# --- Execution ---
    
if __name__ == "__main__":
    # Define paths 
    parser = argparse.ArgumentParser(description="Render 3D model with specified configurations.")
    parser.add_argument("model_path", type=str, help="Path to the 3D model file (e.g., .glb, .usdc).")
    parser.add_argument("output_dir", type=str, help="Directory to save the rendered images.")

    args = parser.parse_args()
    
    # Define paths from CLI arguments
    MODEL_PATH = args.model_path
    OUTPUT_DIR = args.output_dir

    # Base configurations
    render_config = RenderConfig(
        resolution=256,
        samples=128,
        background=Background.TRANSPARENT,
    )

    lighting_config = LightingConfig(
        num_lights=2,
        light_setup=LightSetup.OVERHEAD,
        light_intensity=0.5,
        light_type=LightType.SUN
    )

    camera_config = CameraConfig(
        distance=1,
        min_elevation=0,
        max_elevation=45,
        roll=0.0,
        camera_path_type=CameraPathType.SPIRAL_PHI,
        camera_density=16, # NB: outputs 8 images if .HALF coverage
        angular_step=30.0, # not needed for sprial phi
        sphere_coverage=SphereCoverage.HALF
    )

    blend_config = BlendFileConfig(
        keep_lights=False,
        keep_materials=True,
        keep_world_settings=False
    )

    # Run single test
    run_render_test(
        model_path=MODEL_PATH,
        output_dir=OUTPUT_DIR,
        render_config=render_config,
        lighting_config=lighting_config,
        camera_config=camera_config,
        blend_config=blend_config
    )

