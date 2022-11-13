

"""
Setup script.

Use this script to install the RASA NLU module of the retico simulation framework.
Usage:
    $ python3 setup.py install
The run the simulation:
    $ retico [-h]
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    "description": "The RASA NLU incremental module for the retico framework",
    "author": "Ryan Pacheco, Casey Kennington, Enoch Levandovsky",
    "url": "??",
    "download_url": "??",
    "author_email": "caseykennington@boisestate.edu, enochlev@gmail.com",
    "version": "1.0",
    "install_requires": ["retico-core~=0.2.0", "rasa~=3.2"],
    "packages": find_packages(),
    "name": "retico-rasa-nlu",
}

setup(**config)