from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()


setup(
    name="ICARUS Edge detector",
    version="0.1.0",
    packages=find_packages(include=["detector"]),
    install_requires=required_packages,
)
