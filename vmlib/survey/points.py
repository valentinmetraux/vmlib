# -*- coding: utf-8 -*-

"""
This modules contains classes and methods related to each individual
topographical survey points.
"""


class Survey_point(object):

    """
    Store and operates on individual survey points.survey

    Parameters
    ----------
    project: str
        Project name

    site: str or int
        Sitename or number. Is converted to string

    line: str or int
        Line name. Is converted to string

    method: str
        Method name ['rx', 'rf', 'ert' 'em', 'grav', 'other']

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

    azimtuh:    float or int
        Azimuth of the line at the point's location

    offset_inline: float or int
        Inline offset between preplot and postplot coordinates

    offset_crossline: float or int
        Crossline offset between preplot and postplot coordinates

    offset_abd: float or int
        Absolute offset

    note: str
        Any note or remark on the point.
    """

    def __init__(self, project='', site='', line='', method='', point_type='',
                   point_id='', status='raw', preplot=(0, 0),
                   postplot=(0, 0, 0), kp_ref=(0, 0), distance=0,
                   instrument='', initials='Unknown', crs='', azimuth=0,
                   offset_inline=0, offset_crossline=0, offset_abd= 0,
                   note=''):
        self.project = str(project)
        self.site = str(site)
        self.line = str(line)
        self.method = str(method)
        self.point_id = str(point_id)
        self.point_type = str(point_type)
        self.status = str(status)
        self.preplot = (float(x) for x in preplot)
        self.postplot = [float(x) for x in postplot]
        self.kp_ref = [float(x) for x in kp_ref]
        self.distance = 0
        self.instrument = str(instrument)
        self.surveyor_initials = str(initials)
        self.crs = str(crs)
        self.azimuth = 0
        self.offset_inline = 0
        self.offset_crossline = 0
        self.offset_abs = 0
        self.note = str(note)


    def __str__(self):
        return f'Site {self.site} - Line {self.line} - {self.point_type.upper()} - Point {self.point_id} - {self.status.upper()}'


    def __repr__(self):
        return f'Site {self.site} - Line {self.line} - {self.point_type.upper()} - Point {self.point_id} - {self.status.upper()} - {self.note}'
