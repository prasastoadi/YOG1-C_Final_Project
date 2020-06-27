from setuptools import setup, find_packages

setup(
    name='ctbangkit',
    version='0.0.2dev',
    description='CTBangkit',
    packages=find_packages(),
    install_requires=[
   'efficientnet==1.1.0',
   'tensorflow>=2.2',
   'tensorflow-hub',
   'dotmap',
   'pandas']
)
