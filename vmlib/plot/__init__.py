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

__all__ = ['boxplot', 'hist', 'lines', 'scatter', 'seis', 'styles']


from .hist import distribution
from .lines import generic, fill
from .scatter import xy_map
from .seis import basemap_line, elevation, offset_cdp_fold, amplitude_offset
from .seis import stacking, fold, cdp_spacing, rms_map, short_gathers


from .styles import set_plot_styles
