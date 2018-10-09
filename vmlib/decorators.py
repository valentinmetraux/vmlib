# -*- coding: utf-8 -*-
import functools
import logging
import time


def set_unit(unit):
    """
    Decorator registering a unit on a function.

    Parameters:
    -----------
    unit: str
        String of the unit name (might be cm^3, GPa, m/s, etc).m

    Raises:
    -------
    None

    Returns:
    --------
    decorator_set_unit: str
        String of the unit name as a function attribute.
    """
    def decorator_set_unit(func):
        func.unit = unit
        return func
    logging.debug("DEBUG")
    logging.info("INFO")
    return decorator_set_unit


def timer(func):
    """
    Decorator print the runtime of a function.

    Parameters:
    -----------
    None

    Raises:
    -------
    None

    Returns:
    --------
    None
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logging.debug(f"{func.__name__!r} has run in {run_time:.3f} secs")
        return value
    return wrapper_timer

