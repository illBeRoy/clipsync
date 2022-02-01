#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name='clipsync',
      version='0.2',
      description='cli for zeroconf shared clipboards over local networks',
      author='Roy Sommer',
      url='https://www.github.com/illberoy/clipsync',
      packages=find_packages(),
      include_package_data=True,
      scripts=['run.py'],
      install_requires=['Twisted==16.4.0',
                        'Klein==15.3.1',
                        'clipboard==0.0.4',
                        'detach==1.0',
                        'netbeacon==1.1',
                        'treq==22.1.0',
                        'pycrypto==2.6.1'],
      entry_points={'console_scripts': ['clipsync = run:main']})
