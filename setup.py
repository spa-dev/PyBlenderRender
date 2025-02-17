from setuptools import setup, find_packages

setup(
    name="PyBlenderRender",
    version="0.2.0",
    author='spa-dev',
    description="A Python package for rendering 3D models using Blender.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    #package_data={
    #    "": ["*.glb"],  # Include .glb files
    #},
    #include_package_data=True,
    install_requires=[
        "numpy",
        "tqdm",
        # List other dependencies here
    ],
    python_requires=">=3.7",
)
