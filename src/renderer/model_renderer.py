# src/renderer/model_renderer.py

import gc        
import math
import os
import sys
import time
from typing import List, Optional
from contextlib import contextmanager, redirect_stdout

import bpy
import numpy as np
from mathutils import Vector
from tqdm import tqdm

from .config.render_config import RenderConfig, Background
from .config.lighting_config import LightingConfig, LightType, LightSetup
from .config.camera_config import CameraConfig
from .config.blend_config import BlendFileConfig
from .utils.coordinates import SphericalCoordinate
from .utils.logger import logger
#from .camera.registry import registry as camera_registry
#from .lighting.registry import registry as lighting_resistry
from .camera import camera_registry
from .lighting import lighting_registry

@contextmanager
def stdout_redirected(to=os.devnull):
    """Suppress Blender's verbose console output.
    
    This function redirects stdout to suppress excessive console logs during 
    rendering. It uses a context manager to ensure that output redirection 
    is safely restored after execution. 

    Note: This helps reducing noise from Blender's logs but should be used 
    cautiously in debugging scenarios where console output is required.
    """

    with open(to, 'w') as file, redirect_stdout(file):
        yield

class ModelRenderer:
    """A class for rendering 3D models with configurable camera paths,  
    lighting, and render settings.
    
    Provides functionality to render 3D models using Blender's Cycles engine,
    supporting multiple camera path types, lighting configurations, and render settings.
    The renderer handles multiple file formats and can generate multiple views
    based on configurable camera paths and lighting setups.
    
    Parameters
    ----------
    blend_config : BlendFileConfig, optional
        Configuration for handling .blend file settings:
        - keep_lights: Whether to preserve existing lights (default: False)
        - keep_materials: Whether to preserve existing materials (default: True)
        - keep_world_settings: Whether to preserve world settings (default: False)
        If not provided, uses default BlendFileConfig settings.
        
    render_config : RenderConfig, optional
        Configuration for rendering settings:
        - resolution: Output resolution in pixels (default: 1024)
        - samples: Number of render samples (default: 128)
        - device: Render device, "GPU" or "CPU" (default: "GPU")
        - use_denoising: Whether to use denoising (default: True)
        - background: Background type (Background.WHITE or Background.TRANSPARENT)
        If not provided, uses default RenderConfig settings.
    
    lighting_config : LightingConfig, optional
        Configuration for scene lighting:
        - num_lights: Number of lights in scene (default: 1; maximum: 8)
        - light_type: Type of light (LightType.AREA, SUN, POINT, or SPOT)
        - light_height: Height of lights above center (default: 3.0)
        - light_radius: Radius for light positioning (default: 5.0)
        - light_setup: Light arrangement (default: LightSetup.RANDOM_FIXED)
        - light_intensity: Light strength (default: 0.5)
        If not provided, uses default LightingConfig settings.
    
    camera_config : CameraConfig, optional
        Configuration for camera settings and path generation:
        - distance: Camera distance from center (default: 1.0)
        - min_elevation: Minimum vertical angle (default: -90.0)
        - max_elevation: Maximum vertical angle (default: 90.0)
        - roll: Camera roll angle (default: 0.0)
        - camera_path_type: Type of camera path (default: CameraPathType.CUBE)
        - camera_density: Number of cameras for orbit and phi spiral (default: 35)
        - angular_step: Base angular step for linear and phased spiral (default: 45.0)
        - sphere_coverage: Camera coverage (SphereCoverage.FULL or SphereCoverage.HALF)
        If not provided, uses default CameraConfig settings.
    
    Methods
    -------
    render(model_path: str, output_dir: str) -> None
        Render the model from multiple angles based on the camera path configuration
        and save to the specified output directory. The output filenames include
        camera position information (azimuth, elevation, roll).
        
    get_render_stats() -> dict
        Return statistics about the last render operation, including:
        - total_renders: Total number of renders attempted
        - successful_renders: Number of successful renders
        - failed_renders: Number of failed renders
        - render_time: Total time taken for rendering
        - output_directory: Directory where renders were saved
    
    Examples
    --------
    >>> renderer = ModelRenderer(
    ...     render_config=RenderConfig(resolution=(300,600), samples=256),
    ...     camera_config=CameraConfig(
    ...         camera_path_type=CameraPathType.SPIRAL_PHI,
    ...         camera_density=50
    ...     )
    ... )
    >>> renderer.render("model.glb", "output_renders")
    >>> stats = renderer.get_render_stats()
    
    Notes
    -----
    - When importing .blend files, existing scene elements may be preserved
      or replaced based on the BlendFileConfig settings.
    - Camera paths and lighting setups are handled by generators.
    - If SphereCoverage.HALF is specified, camera_density will be half 
      that expected.
    - Blender console output messages are discarded.
    """
    
    def __init__(
        self,
        blend_config: Optional[BlendFileConfig] = None,
        render_config: Optional[RenderConfig] = None,
        lighting_config: Optional[LightingConfig] = None,
        camera_config: Optional[CameraConfig] = None
    ):
        """Initialize the ModelRenderer with configuration objects."""
        self.blend_config = blend_config or BlendFileConfig()
        self.render_config = render_config or RenderConfig()
        self.lighting_config = lighting_config or LightingConfig()
        self.camera_config = camera_config or CameraConfig()
        self.render_stats = {}
        
    def _setup_scene(self) -> None:
        """Configure the basic scene settings and render engine."""
        #  Configure engine
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.samples = self.render_config.samples
        bpy.context.scene.cycles.use_adaptive_sampling = True
        bpy.context.scene.cycles.use_denoising = self.render_config.use_denoising
        
        #  Untested alternatives:     
        #  bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        #  bpy.context.scene.eevee.use_ssr = True  # Enable screen-space reflections
        #  bpy.context.scene.eevee.use_bloom = True  # Enable bloom for glow effects

        if self.render_config.device == "GPU":
            bpy.context.scene.cycles.device = 'GPU'
            #  bpy.context.preferences.addons["cycles"].preferences.compute_device_type = \
            #      "CUDA"  # or "HIP" for AMD

        bpy.context.scene.render.resolution_x = self.render_config.resolution_x
        bpy.context.scene.render.resolution_y = self.render_config.resolution_y
        bpy.context.scene.render.film_transparent = (
            self.render_config.background == Background.TRANSPARENT
        )
      
        # Configure world settings
        world = bpy.context.scene.world or bpy.data.worlds.new("World")
        bpy.context.scene.world = world
        world.use_nodes = True
        bg = world.node_tree.nodes["Background"]
        bg.inputs[0].default_value = (
            (1, 1, 1, 1) if self.render_config.background == Background.WHITE 
            else (0, 0, 0, 0)
        )
        bg.inputs[1].default_value = self.lighting_config.light_intensity

        # Check materials
        for obj in bpy.context.scene.objects:
            if obj.type == "MESH" and not obj.data.materials:
                logger.warning(f"Object {obj.name} has no materials!")

    def _import_model(self, filepath: str) -> None:
        """Import 3D model based on file extension."""

        # Clear scene. TODO: refactor to self._clear_scene()
        # Remove all objects except the world settings.
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        # Remove orphaned meshes, materials, etc.
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
            
        ext = os.path.splitext(filepath)[1].lower()

        if ext == '.blend':
            bpy.ops.wm.open_mainfile(filepath=filepath)
            self._handle_blend_file_settings()
            return
        
        importers = {
            '.dae': lambda: bpy.ops.wm.collada_import(filepath=filepath),
            '.glb': lambda: bpy.ops.import_scene.gltf(filepath=filepath),
            '.gltf': lambda: bpy.ops.import_scene.gltf(filepath=filepath),
            '.usdc': lambda: bpy.ops.wm.usd_import(filepath=filepath)
        }
        
        importer = importers.get(ext)
        if not importer:
            raise ValueError(f"Unsupported file format: {ext}")
            
        importer()
        
        if not bpy.context.selected_objects:
            raise RuntimeError("No objects were imported from the model file")

        # Center and scale model
        for obj in bpy.context.selected_objects:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj    
        
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        #  Options include type='ORIGIN_CENTER_OF_MASS', center='MEDIAN', or others

        #  Align model to X axis (buggy)
        #  bpy.ops.object.transform_apply(rotation=True)
        #  bpy.context.active_object.rotation_euler = (0, 0, 0)

    def _handle_blend_file_settings(self) -> None:
        """Handle configuration differences between .blend file and renderer settings."""
        scene = bpy.context.scene
        
        # Handle render settings
        if self.render_config.device == "GPU":
            scene.cycles.device = 'GPU'
        scene.render.resolution_x = self.render_config.resolution_x
        scene.render.resolution_y = self.render_config.resolution_y
        scene.cycles.samples = self.render_config.samples
        scene.cycles.use_denoising = self.render_config.use_denoising
        scene.render.film_transparent = (
            self.render_config.background == Background.TRANSPARENT
        )
    
        # Handle existing lights
        existing_lights = [obj for obj in scene.objects if obj.type == 'LIGHT']
        if not self.blend_config.keep_lights:
            for light in existing_lights:
                bpy.data.objects.remove(light, do_unlink=True)
        # Add more sophisticated light handling here if needed

        # Handle materials (if not keeping materials, remove them)
        if not self.blend_config.keep_materials:
            for material in bpy.data.materials:
                bpy.data.materials.remove(material, do_unlink=True)
                
        # Remove cameras (always remove existing cameras)
        existing_camera = next((obj for obj in scene.objects if obj.type == 'CAMERA'), None)
        if existing_camera:
            bpy.data.objects.remove(existing_camera, do_unlink=True)
        
        # Handle world settings
        if not self.blend_config.keep_world_settings:
            world = scene.world
            if world and world.use_nodes:
                background_node = world.node_tree.nodes.get("Background")
                if background_node:
                    if self.render_config.background == Background.WHITE:
                        background_node.inputs[0].default_value = (1, 1, 1, 1)
                    else:
                        background_node.inputs[0].default_value = (0, 0, 0, 0)
                    background_node.inputs[1].default_value = self.lighting_config.light_intensity

    def _setup_camera(self) -> bpy.types.Object:
        """Create and configure camera with tracking."""
        camera = bpy.data.objects.get("Camera")
        if not camera:
            bpy.ops.object.camera_add()
            camera = bpy.context.active_object
            camera.name = "Camera"
    
        bpy.context.scene.camera = camera

        # Set up object tracking
        objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
        if not objects:
            raise RuntimeError("No mesh objects found in the scene to focus on")
    
        target = objects[0]
        
        # Warning: TRACK_TO causes problems with camera rotation at poles:
        #track_constraint = (
        #    camera.constraints.get("Track To") or 
        #    camera.constraints.new(type='TRACK_TO')
        #)
        #track_constraint.target = target
        #track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        #track_constraint.up_axis = 'UP_Y'

        # "DAMPED_TRACK" to avoid gimbal lock and instability near poles.
        # Has issues with maintaining a uniform distance from all angles.
        track_constraint = (
            camera.constraints.get("Damped Track") or 
            camera.constraints.new(type='DAMPED_TRACK')
        )
        track_constraint.target = target
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'  # No up_axis needed?

        return camera

    def _position_camera(self, camera: bpy.types.Object, coord: SphericalCoordinate) -> None:
        """Position and orient camera based on spherical coordinates."""
        az_rad = math.radians(coord.azimuth)
        el_rad = math.radians(coord.elevation)
        roll_rad = math.radians(coord.roll)

        #  Spherical to Cartesian Conversion (Z-up)
        x = coord.radius * math.cos(el_rad) * math.sin(az_rad)
        y = coord.radius * math.cos(el_rad) * math.cos(az_rad)
        z = coord.radius * math.sin(el_rad)

        camera.location = Vector((x, y, z))
        
        direction = -camera.location.normalized()
        rot_quat = direction.to_track_quat('-Z', 'Y')
        euler = rot_quat.to_euler('XYZ')
        
        camera.rotation_mode = 'XYZ'
        camera.rotation_euler = euler
        camera.rotation_euler.rotate_axis('Z', roll_rad)
        
    def _generate_camera_positions(self) -> List[SphericalCoordinate]:
        """Generate camera positions based on the selected path type."""
        path_type = self.camera_config.camera_path_type.value
        generator = camera_registry.get_generator(path_type)
        # Return camera positions
        return generator.generate_positions(self.camera_config)

    def _setup_lighting(self) -> List[bpy.types.Object]:
        """Create lighting setup based on configuration."""
        setup_class = lighting_registry.get_setup(self.lighting_config.light_setup.value)
        self.light_setup = setup_class(self.lighting_config)
        return self.light_setup.create_lights()

    def render(self, model_path: str, output_dir: str) -> None:
        """Render the model from multiple angles and save to output directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            start_time = time.time()
            
            self._setup_scene()
            self._import_model(model_path)
                          
            camera = self._setup_camera()            
            lights = self._setup_lighting()
            
            camera_positions = self._generate_camera_positions()           
            total_renders = len(camera_positions)
            successful_renders = 0
            
            logger.info(f"Starting render of {total_renders} images...")

            with tqdm(total=total_renders, desc="Rendering", unit="frame") as pbar:
                for i, coord in enumerate(camera_positions):
                    self._position_camera(camera, coord)
                    
                    # Delegate light position updates to the setup
                    self.light_setup.update_positions(coord.azimuth)
                    # Each setup class handles this differently:
                    # - RandomDynamicSetup: repositions lights based on camera angle
                    # - RandomFixedSetup: does nothing (lights stay in initial positions)
                    # - OverheadSetup: does nothing (lights stay overhead)
                    
                    output_path = os.path.join(
                        output_dir, 
                        f"render_{i:03d}_az{coord.azimuth:03.0f}_el{coord.elevation:03.0f}"
                        f"_roll{coord.roll:03.0f}.png"
                    )
                    bpy.context.scene.render.filepath = output_path
       
                    logger.debug(
                        f"Frame {i}: Azimuth={coord.azimuth}, "
                        f"Elevation={coord.elevation}, Roll={coord.roll}"
                    )

                    with stdout_redirected():  # Suppress Blender output during render
                        try:
                            bpy.ops.render.render(write_still=True)
                            successful_renders += 1
                        except Exception as e:
                            logger.error(f"Failed to render position {i}: {str(e)}")
                    # Update progress bar
                    pbar.update(1)
                    
            logger.info(f"Completed {total_renders} renders.")
            
            end_time = time.time()
            
            self.render_stats = {
                'total_renders': total_renders,
                'successful_renders': successful_renders,
                'failed_renders': total_renders - successful_renders,
                'render_time': end_time - start_time,
                'output_directory': output_dir
            }
            
        except Exception as e:
            raise RuntimeError(f"Render operation failed: {str(e)}")

        finally:
            # Ensure all objects are removed
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
            # Reset Blender scene to factory settings
            bpy.ops.wm.read_factory_settings(use_empty=True)
            logger.info("Blender scene reset to factory settings.")
            # Clear renderer variables and memory
            del camera, lights, camera_positions
            gc.collect()

    def get_render_stats(self) -> dict:
        """Return statistics about the last render operation."""
        return self.render_stats
