# -*- coding: utf-8 -*-

"""Top-level package for vmlib."""

__author__ = """Valentin Metraux"""
__email__ = 'valentin@valentinmetraux.com'
__version__ = '0.3.0'
__license__ = 'MIT'
__docformat__ = 'reStructuredText'


__all__ = ['decorators', 'dirs', 'em', 'ert', 'gis', 'hydrology', 'io',
           'math', 'pdf', 'plot', 'project', 'seismic', 'stats', 'survey',
           'tools', 'units', 'utils']

# Standard libtrary imports
import logging
import sys

# Third party imports

# Local imports
from .decorators import *
from .custom_exceptions import *
from . import dirs
from . import em
from . import ert
from . import gis
from . import hydrology
from . import io
from . import math
from . import pdf
from . import plot
from . import project
from . import seismic
from . import stats
from . import survey
from . import tools
from . import units
from . import utils


# Set library-wide shared parameters
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
sys.tracebacklimit = 3
