# -*- coding: utf-8 -*-
from .constants import pi


def convert_temperature(val, old_scale="fahrenheit", new_scale="celsius"):
    """
    Convert from a temperatuure scale to another one among Celsius, Kelvin
    and Fahrenheit.

    Parameters
    ----------
    val: float or int
        Value of the temperature to be converted expressed in the original
        scale.

    old_scale: str
        Original scale from which the temperature value will be converted.
        Supported scales are Celsius ['Celsius', 'celsius', 'c'],
        Kelvin ['Kelvin', 'kelvin', 'k'] or Fahrenheit ['Fahrenheit',
        'fahrenheit', 'f'].

    new_scale: str
        New scale from which the temperature value will be converted.
        Supported scales are Celsius ['Celsius', 'celsius', 'c'],
        Kelvin ['Kelvin', 'kelvin', 'k'] or Fahrenheit ['Fahrenheit',
        'fahrenheit', 'f'].

    Raises
    -------
    NotImplementedError if either of the scales are not one of the requested
    ones.

    Returns
    -------
    res: float
        Value of the converted temperature expressed in the new scale.
    """
    # Convert from 'old_scale' to Kelvin
    if old_scale.lower() in ['celsius', 'c']:
        temp = val + 273.15
    elif old_scale.lower() in ['kelvin', 'k']:
        temp = val
    elif old_scale.lower() in ['fahrenheit', 'f']:
        temp = 5.0 * (val - 32) / 9.0 + 273.15
    else:
        raise AttributeError(
            f'{old_scale} is unsupported. Celsius, Kelvin and Fahrenheit are supported')
    # and from Kelvin to 'new_scale'
    if new_scale.lower() in ['celsius', 'c']:
        result = temp - 273.15
    elif new_scale.lower() in ['kelvin', 'k']:
        result = temp
    elif new_scale.lower() in ['fahrenheit', 'f']:
        result = (temp - 273.15) * 9.0 / 5.0 + 32
    else:
        raise AttributeError(
            f'{new_scale} is unsupported. Celsius, Kelvin and Fahrenheit are supported')
    return result


def convert_distance(val, old_scale="meter", new_scale="centimeter"):
    """
    Convert from a length scale to another one among meter, centimeter, inch,
    feet, and mile.

    Parameters
    ----------
    val: float or int
        Value of the length to be converted expressed in the original scale.

    old_scale: str
        Original scale from which the length value will be converted.
        Supported scales are Meter ['Meter', 'meter', 'm'],
        Centimeter ['Centimeter', 'centimeter', 'vm'], Inch ['Inch', 'inch', 'in'], Feet ['Feet', 'feet', 'ft'] or Mile ['Mile', 'mile', 'mil'].

    new_scale: str
        New scale from which the length value will be converted.
        Supported scales are Meter ['Meter', 'meter', 'm'],
        Centimeter ['Centimeter', 'centimeter', 'cm'], Inch ['Inch', 'inch', 'in'], Feet ['Feet', 'feet', 'ft'] or Mile ['Mile', 'mile', 'mil'].

    Raises
    -------
    NotImplementedError if either of the scales are not one of the requested
    ones.

    Returns
    -------
    res: float
        Value of the converted length expressed in the new scale.
    """
    # Convert from 'old_scale' to Meter
    if old_scale.lower() in ['centimeter', 'cm']:
        temp = val / 100.0
    elif old_scale.lower() in ['meter', 'm']:
        temp = val
    elif old_scale.lower() in ['inch', 'in']:
        temp = val / 39.37008
    elif old_scale.lower() in ['feet', 'ft']:
        temp = val / 3.28084
    elif old_scale.lower() in ['mile', 'mil']:
        temp = 1609.344 * val
    else:
        raise AttributeError(
            f'{old_scale} is unsupported. m, cm, ft, in and mile are supported')
    # and from Meter to 'new_scale'
    if new_scale.lower() in ['centimeter', 'cm']:
        result = 100*temp
    elif new_scale.lower() in ['meter', 'm']:
        result = temp
    elif new_scale.lower() in ['inch', 'in']:
        result= 39.37008*temp
    elif new_scale.lower() in ['feet', 'ft']:
        result=3.28084*temp
    elif new_scale.lower() in ['mile', 'mil']:
        result=temp/1609.344
    else:
        raise AttributeError(
            f'{new_scale} is unsupported. m, cm, ft, in and mile are supported')
    return result


def convert_weight(val, old_scale="kg", new_scale="pound"):
    """
    Convert from a weight scale to another one among kg, gram, and pound.

    Parameters
    ----------
    val: float or int
        Value of the weight to be converted expressed in the original scale.

    old_scale: str
        Original scale from which the weight value will be converted.
        Supported scales are Kilogram ['Kilogram', 'kilogram', 'kg'],
        Gram ['Gram', 'gram', 'gr'] or Pound ['Pound', 'pound', 'pd'].

    new_scale: str
        New scale from which the weight value will be converted.
        Supported scales are Kilogram ['Kilogram', 'kilogram', 'kg'],
        Gram ['Gram', 'gram', 'gr'] or Pound ['Pound', 'pound', 'pd'].

    Raises
    -------
    NotImplementedError if either of the scales are not one of the requested
    ones.

    Returns
    -------
    res: float
        Value of the converted weight expressed in the new scale.
    """
    # Convert from 'old_scale' to Kg
    if old_scale.lower() in ['kilogram', 'kg']:
        temp = val
    elif old_scale.lower() in ['gram', 'gr']:
        temp = val / 1000.0
    elif old_scale.lower() in ['pound', 'pd']:
        temp = 0.4535924 * val
    else:
        raise AttributeError(
            f'{old_scale} is unsupported. kg, gr, and pound are supported')
    # and from kg to 'new_scale'
    if new_scale.lower() in ['kilogram', 'kg']:
        result = temp
    elif new_scale.lower() in ['gram', 'gr']:
        result = 1000 * temp
    elif new_scale.lower() in ['pound', 'pd']:
        result= temp / 0.4535924
    else:
        raise AttributeError(
            f'{new_scale} is unsupported. kg, gr, and pound are supported')
    return result


def convert_angle(val, old_scale="kg", new_scale="pound"):
    """
    Convert from a angle scale to another one among degree, and radias.

    Parameters
    ----------
    val: float or int
        Value of the angle to be converted expressed in the original scale.

    old_scale: str
        Original scale from which the angle value will be converted.
        Supported scales are Degree ['Degree', 'degree', 'deg'] or Radian ['Radian', 'radian', 'rad'].

    new_scale: str
        New scale from which the angle value will be converted.
         Supported scales are Degree ['Degree', 'degree', 'deg'] or Radian ['Radian', 'radian', 'rad'].

    Raises
    -------
    NotImplementedError if either of the scales are not one of the requested
    ones.

    Returns
    -------
    res: float
        Value of the converted angle expressed in the new scale.
    """
    # Convert from 'old_scale' to degrees
    if old_scale.lower() in ['degree', 'deg']:
        temp = val
    elif old_scale.lower() in ['radian', 'rad']:
        temp = val * 180 / pi
    else:
        raise AttributeError(
            f'{old_scale} is unsupported. Degree and radian are supported')
    # and from degrees to 'new_scale'
    if new_scale.lower() in ['degree', 'deg']:
        result = temp
    elif new_scale.lower() in ['radian', 'rad']:
        result = temp * pi / 180
    else:
        raise AttributeError(
            f'{new_scale} is unsupported. Degree and radian are supported')
    return result


def convert_velocity(val, old_scale="km/h", new_scale="m/s"):
    """
    Convert from a velocity scale to another one among km/h, and m/s.

    Parameters
    ----------
    val: float or int
        Value of the velocity to be converted expressed in the original scale.

    old_scale: str
        Original scale from which the angle value will be converted.
        Supported scales are km/h or m/s.

    new_scale: str
        New scale from which the angle value will be converted.
         Supported scales are km/h or m/s.

    Raises
    -------
    NotImplementedError if either of the scales are not one of the requested
    ones.

    Returns
    -------
    res: float
        Value of the converted velocity expressed in the new scale.
    """
    # Convert from 'old_scale' to m/s
    if old_scale == 'm/s':
        temp = val
    elif old_scale == 'km/h':
        temp = val * 3.6
    else:
        raise AttributeError(
            f'{old_scale} is unsupported. km/h and m/s are supported')
    # and from m/s to 'new_scale'
    if new_scale == 'm/s':
        result = temp
    elif new_scale == 'km/h':
        result = temp / 3.6
    else:
        raise AttributeError(
            f'{new_scale} is unsupported. km/h and m/s are supported')
    return result
