"""
Python setup file for cryptostats
"""

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='cryptostats',
    version='0.1.0',
    packages=['cryptostats'],
    include_package_data=True,
    install_requires=requirements
)
