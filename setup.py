from setuptools import find_packages
from setuptools import setup
with open('./requirements.txt') as f:
    required = f.read().splitlines()
setup(
    name='visualize',
    version='0.0.1',
    author='Ramil B',
    install_requires=required,
    packages=find_packages()
)
