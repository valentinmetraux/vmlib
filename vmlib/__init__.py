# -*- coding: utf-8 -*-

"""Top-level package for vmlib."""

__author__ = """Valentin Metraux"""
__email__ = 'valentin@valentinmetraux.com'
__version__ = '0.2.2'
__license__ = 'MIT'
__docformat__ = 'reStructuredText'

__all__ = ["decorators","dir", "hydrology", "io", "math", "pdf", "plot", "survey", "units",]

# Standard libtrary imports
import logging

# Third party imports

# Local imports
from .decorators import *
from . import units
from . import survey

# Set library-wide shared parameters
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
    )

