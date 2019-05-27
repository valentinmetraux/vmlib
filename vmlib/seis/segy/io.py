# -*- coding: utf-8 -*-
import pathlib
import segyio
import vmlib as vm


class Segy():

    def __init__(self, path=''):
        with segyio.open(filename=path, mode='r', ignore_geometry=True) as f:
            self.info = vm.seis.segy.info.build(f)
        self.info['filename'] = pathlib.Path(path).name
        self.info['file'] = pathlib.Path(path)
        self.info['filepath'] = pathlib.Path(path).parent

    def __str__(self):
        return f"SEGY - {self.info['file']} - {self.info['n_traces']} traces"

    def cut(self, cut_time=1000, outpath=pathlib.Path.cwd()):
        cut_file = vm.seis.segy.edit.cut(self, cut_time, outpath)
        return cut_file

    def resample(self, sample_rate=4, outpath=pathlib.Path.cwd()):
        resampled_file = vm.seis.segy.edit.resample(self, sample_rate, outpath)
        return resampled_file

    def export_headers(self, format='csv'):
        pass

    def get_trace_stats(self):
        pass

    def sort(self):
        pass



# Class 2DSection with plot method



# Base class for SEGY in vmlib
# Subclass for each segytype
    # 2D prestack
    # 2D poststack
    # 3D prestack
    # 3D poststack
