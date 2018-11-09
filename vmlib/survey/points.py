# -*- coding: utf-8 -*-

"""
This modules contains classes and methods related to each individual
topographical survey points.
"""
import logging
from ..custom_exceptions import *


class Survey_point(object):

    """
    Store and operates on individual survey points.survey

    Parameters
    ----------
    point_type: str
        Point type ['src', 'rcv', 'electrode', 'em', 'grav', 'other']

    point_id: str or int

    status: str
        Point status ['raw', 'qc', 'final']

    preplot: tuple
        Preplot coordinates as a (x, y) tuple of floats/ints

    postplot: tuple
        Postplot coordinates as a (x, y, z) tuple of floats/ints

    kp_ref: tuple
        Coordinates of the reference kp point as a (x, y) tuple of floats/ints

    distance: float or int
        Distance from kp_ref

    instrument: str
        Survey instrument used

    initials:   str
        Surveyor initials

    crs:    str or int
        Coordinate reference system code (EPSG)

    azimuth:    float or int
        Azimuth of the line at the point's location

    offset_inline: float or int
        Inline offset between preplot and postplot coordinates

    offset_crossline: float or int
        Crossline offset between preplot and postplot coordinates

    offset_abd: float or int
        Absolute offset

    note: str
        Any note or remark on the point.

    Methods:
    --------
    compute_distance("preplot" or "postplot")
    compute_offsets()
    ensure_point_type_coherency()
    """

    def __init__(self, point_type='', point_id='', status='raw',
                 preplot=(0, 0), postplot=(0, 0, 0), kp_ref=(0, 0), distance=0,
                 instrument='', initials='Unknown', crs='', azimuth=0,
                 offset_inline=0, offset_crossline=0, offset_abd=0,
                 note=''):
        # Parameter check and instance parameters instanciation
        if isinstance(project, str):
            self.project = str(project)
        else:
            logging.critical('Type error on project argument')
            raise TypeError("SCRIPT TERMINATED")
        if isinstance(site, (str, int)):
            self.site = str(site)
        else:
            logging.critical('Type error on site argument')
            raise TypeError("SCRIPT TERMINATED")
        if isinstance(line, (str, int)):
            self.line = str(line)
        else:
            logging.critical('Type error on line argument')
            raise TypeError("SCRIPT TERMINATED")
        if method in ['rx', 'rf', 'ert' 'em', 'grav', 'other']:
            self.method = str(method)
        else:
            logging.critical('Method should be in ["rx", "rf", "ert", "em", "grav", "other"]')
            raise TypeError("SCRIPT TERMINATED")
        self.point_id = str(point_id)
        self.point_type = str(point_type)
        self.status = str(status)
        self.preplot = (float(x) for x in preplot)
        self.postplot = [float(x) for x in postplot]
        self.kp_ref = [float(x) for x in kp_ref]
        self.distance = 0
        self.instrument = str(instrument)
        if isinstance(note, str):
            self.surveyor_initials = str(initials)
        else:
            logging.critical('Type error on initials argument')
            raise TypeError("SCRIPT TERMINATED")
        self.crs = str(crs)
        self.azimuth = 0
        self.offset_inline = 0
        self.offset_crossline = 0
        self.offset_abs = 0
        if isinstance(note, str):
            self.note = str(note)
        else:
            logging.critical('Type error on note argument')
            raise TypeError("SCRIPT TERMINATED")

    def __str__(self):
        return f'Site {self.site} - Line {self.line} - {self.point_type.upper()} - Point {self.point_id} - {self.status.upper()}'

    def __repr__(self):
        return f'Site {self.site} - Line {self.line} - {self.point_type.upper()} - Point {self.point_id} - {self.status.upper()} - {self.note}'
