# -*- coding: utf-8 -*-

"""
=========================
Constants (mod: 'vmlib.units')
=========================
Physical and mathematical constants and units

Mathematical constants
=========================
pi, golden_ratio

Physical constants
=========================
c, G, g

Densities
=========================
water_density

Converter funnctions
=========================
convert_temperature(val, old_scale, new_scale)
convert_distance(val, old_scale, new_scale)
convert_weigth(val, old_scale, new_scale)
convert_angle(val, old_scale, new_scale)
convert_velocity(val, old_scale, new_scale)

"""

__all__ = ['constants', 'converter']

from .constants import *
from .converter import *


