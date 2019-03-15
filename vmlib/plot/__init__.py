# -*- coding: utf-8 -*-

"""
=========================
scatter (mod: 'vmlib.plot')
=========================
xy_map

=========================
hist (mod: 'vmlib.plot')
=========================
distribution

=========================
lines (mod: 'vmlib.plot')
=========================
distribution

"""

__all__ = ['boxplot', 'hist', 'lines', 'scatter', 'styles']


from .hist import distribution
from .lines import generic
from .scatter import xy_map


from .styles import set_plot_styles
