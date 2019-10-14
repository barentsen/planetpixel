#!/usr/bin/env python
import os
import sys
from setuptools import setup

# Prepare and send a new release to PyPI
if "release" in sys.argv[-1]:
    os.system("python setup.py sdist")
    os.system("twine upload dist/planetpixel*")
    os.system("rm -rf dist/planetpixel*")
    sys.exit()

# Load the __version__ variable without importing the package already
exec(open('planetpixel/version.py').read())

setup(name='planetpixel',
      version=__version__,
      description="Solving the planet's problems, one pixel at a time.",
      long_description=open('README.rst').read(),
      url='https://barentsen.github.io/planetpixel/',
      author='Geert Barentsen',
      author_email='hello@geert.io',
      license='BSD',
      packages=['planetpixel'],
      include_package_data=True,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Documentation",
          "Topic :: Software Development :: Documentation",
          ],
      )
