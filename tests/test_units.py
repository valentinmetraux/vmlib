# -*- coding: utf-8 -*-

"""
Run tests for the units module of vmlib
"""

import pytest
from vmlib import units as _units


def test_convert_temperature():
    assert _units.convert_temperature(0, 'c', 'f') == 32
    assert _units.convert_temperature(0, 'c', 'k') == 273.15
    assert _units.convert_temperature(32, 'f', 'c') == 0
    assert _units.convert_temperature(273.15, 'k', 'f') == 32
    assert _units.convert_temperature(273.15, 'k', 'c') == 0
    with pytest.raises(AttributeError):
        _units.convert_temperature(0, 'b', 'f')
    with pytest.raises(AttributeError):
        _units.convert_temperature(0, 'c', 'b')


def test_convert_distance():
    assert _units.convert_distance(100, 'cm', 'm') == 1
    assert _units.convert_distance(10, 'm', 'm') == 10
    assert _units.convert_distance(39.37008, 'in', 'm') == 1.0
    assert _units.convert_distance(3.28084, 'ft', 'm') == 1.0
    assert _units.convert_distance(1, 'mile', 'm') == 1609.344
    assert _units.convert_distance(1, 'm', 'cm') == 100
    assert _units.convert_distance(1, 'm', 'in') == 39.37008
    assert _units.convert_distance(1, 'm', 'ft') == 3.28084
    assert _units.convert_distance(1609.344, 'm', 'mile') == 1
    with pytest.raises(AttributeError):
        _units.convert_distance(0, 'b', 'f')
    with pytest.raises(AttributeError):
        _units.convert_distance(0, 'cm', 'k')


def test_convert_weight():
    assert _units.convert_weight(100, 'gr', 'kg') == 0.1
    assert _units.convert_weight(10, 'kg', 'kg') == 10
    assert _units.convert_weight(1, 'pound', 'kg') == 0.4535924
    assert _units.convert_weight(3, 'kg', 'gram') == 3000
    assert _units.convert_weight(0.4535924, 'kg', 'pound') == 1.0
    with pytest.raises(AttributeError):
        _units.convert_weight(0, 'b', 'kg')
    with pytest.raises(AttributeError):
        _units.convert_weight(0, 'kg', 'r')


def test_convert_angle():
    assert _units.convert_angle(180, 'deg', 'rad') == _units.pi
    assert _units.convert_angle(10, 'deg', 'deg') == 10
    assert _units.convert_angle(2*_units.pi, 'rad', 'deg') == 360
    with pytest.raises(AttributeError):
        _units.convert_angle(0, 'b', 'deg')
    with pytest.raises(AttributeError):
        _units.convert_angle(0, 'deg', 'e')


def test_convert_velocity():
    assert _units.convert_velocity(1, 'km/h', 'm/s') == 3.6
    assert _units.convert_velocity(10, 'km/h', 'km/h') == 10
    assert _units.convert_velocity(3.6, 'm/s', 'km/h') == 1
    with pytest.raises(AttributeError):
        _units.convert_velocity(0, 'b', 'm/s')
    with pytest.raises(AttributeError):
        _units.convert_velocity(0, 'm/s', 'e')
