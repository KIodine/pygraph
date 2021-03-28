import setuptools


attrs = {
    "name": "pygraph",
    "version": "0.0.1a",
    "description": "Graph related algorithms and data structures in Python.",
    "author": "KIodine",
    "packages": setuptools.find_packages(),
    "python_requires": ">=3.7",

}
# Use `pip install -e .` for develope install.
setuptools.setup(
    **attrs
)