# **PyBlenderRender**
**A modular Python-based rendering pipeline for Blender, designed for automated camera positioning and rendering of 3D models.**

## **Features**

- Modular configuration for camera, lighting, and rendering
- Multiple camera path generation techniques (Spiral, Pole Rotation, Cube, etc.)
- Blender integration for high-quality 3D rendering
- Extensible architecture for custom camera paths

---

## **Installation**

### **Prerequisites**

- **TBD**
- **TBD**
- **TBD**

### **Install Dependencies**

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/PyBlenderRender.git  
cd PyBlenderRender  
pip install -r requirements.txt  
```

---

## **Usage**

### **1. Basic Example: Render with Default Settings**

```python
from src.renderer.model_renderer import ModelRenderer

renderer = ModelRenderer()  # Uses default configs
renderer.render()  # Runs rendering pipeline
```

### **2. Custom Camera Configuration**

```python
from src.renderer.config.camera_config import CameraConfig
from src.renderer.model_renderer import ModelRenderer

custom_camera = CameraConfig(distance=15.0, camera_density=30)
renderer = ModelRenderer(camera_config=custom_camera)
renderer.render()
```

---

## **Project Structure**

```
PyBlenderRender/
├── README.md
├── setup.py
├── requirements.txt
├── src/
│   └── renderer/
│       ├── __init__.py
│       ├── model_renderer.py         # main rendering logic
│       ├── config/
│       │   ├── __init__.py
│       │   ├── blend_config.py       # BlendFileConfig class
│       │   ├── camera_config.py      # CameraConfig class
│       │   ├── lighting_config.py    # LightingConfig class
│       │   └── render_config.py      # RenderConfig class
│       ├── camera/
│       │   ├── __init__.py
│       │   ├── base.py               # Abstract base class for camera paths
│       │   ├── paths/
│       │   │   ├── __init__.py
│       │   │   ├── cube.py
│       │   │   ├── orbit.py
│       │   │   ├── pole_rotation.py
│       │   │   ├── spiral_linear.py
│       │   │   ├── spiral_phased.py
│       │   │   └── spiral_phi.py
│       │   └── registry.py           # Camera path registry/factory
│       └── utils/
│           ├── __init__.py
│           ├── coordinates.py        # SphericalCoordinate class
│           ├── logger.py
│           └── validation.py         # Placeholder function
├── tests/                            # Unit tests
│   ├── __init__.py
│   ├── conftest.py                   # Pytest fixtures
│   ├── test_renderer.py              # Tests for ModelRenderer
│   ├── config/
│   │   ├── test_configs.py           # Tests for configurations
│   ├── test_data/                    # Test assets (i.e., 3D model)
│   │   ├── test_model.glb
├── notebooks/                        # Jupyter Notebooks for experiments
│   ├── visualize_path.ipynb          # Camera path visualization
│
└── .gitignore
```

---

## **Known Issues**

### Camera Distance Variability in CameraPathType.CUBE

With the CUBE camera path type, the bottom view appears closer than others.  
This issue is possibly related to object tracking issues, where the Track  
To constraint might be influencing the final camera position in unexpected  
ways, especially at extreme elevations.

### Light Energy Calculation Inconsistencies

Light energy calculation does not account for all possible light types  
consistently. Try varying `light_intensity` in `LightingConfig` until you  
reach a suitable level.

---

## **Roadmap**

- Multiprocessing – Improve performance by parallel processing of rendering

---

## **Extending the Project**

Want to add a custom camera path?

1. Create a new file in `src/renderer/camera/paths/`, e.g., `custom_path.py`.
2. Subclass `CameraPathGenerator` and implement `generate_positions()`.
3. Register it in `camera/registry.py`.

---

## **Contributing**

Contributions are welcome! Feel free to submit issues or pull requests. 
This project is a low priority for me, so please accept my apologies in
advance for slow responses.

---

## Attributions

The test model is used under the Creative Commons Attribution 4.0 License:

- **Rubik's Cube** (https://skfb.ly/opCGZ) by BeyondDigital  
  Licensed under Creative Commons Attribution (CC BY 4.0)  
  [License Details](http://creativecommons.org/licenses/by/4.0/)

---

## **License**

📜 MIT License – Free to use and modify. Test model is under CC BY 4.0 (see above).

