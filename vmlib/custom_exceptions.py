# -*- coding: utf-8 -*-


class SimpleExitException(Exception):
    """
    Custom exception showing a simple exit program message
    """
    def __init__(self):
        pass


    def __str__(self):
        return 'Script terminated'.upper()


    def __repr__(self):
        return ''
