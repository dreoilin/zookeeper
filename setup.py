# import os
import re
from setuptools import setup, find_packages

__version__ = None

with open('zookeeper/__version__.py') as version_file:
    # extracts first instance of __version__ = NUMBER in __version__.py
    __version__ = re.findall("__version__ = '([^']*)'", version_file.read())[0]
    
extras_require  = {
    "USB" : ["pyusb>=1.0.2",
             "libusb==1.0"],
    "ASRL" : ["pyserial>=3.4"],
    "SIM" : ["pyvisa-sim"]
    }

setup(
      name="zookeeper",
      version=__version__,
      packages=find_packages(),
      extras_require = extras_require,
      install_requires=["pyvisa>=1.10.1",
                  	"pyvisa-py>=0.4.1",
                        "python-vxi11>=0.9"
                        ],
      author="Cian O'Donnell",
      author_email="cian.odonnell@tyndall.ie",
      description="See README.md"
      # entry_points
      )
