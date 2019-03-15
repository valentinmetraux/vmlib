# -*- coding: utf-8 -*-
import re
import pandas as pd
import segyio


class Segy():

    def __init__(self):
        self.bin_header = {}
        self.text_header = {}
        self.trace_header = ''
        self.data = []
        self.stats = {}

    def __str__(self):
        s = self.stats
        return f"SEGY data - {s['filename']} - {s['n_traces']} traces"

    def load(self, filename, data=True):
        with segyio.open(filename, 'r', ignore_geometry=True) as f:
            f.mmap()
            # Load bin headers
            self.bin_header = f.bin
            # Load text headers
            self.text_header = self.parse_text_header(f)
            # Load data
            if data:
                self.data = f.trace.raw[:]
            # Load stats
            self.stats = {
                'filename': filename,
                'n_traces': f.tracecount,
                'sample_rate': segyio.tools.dt(f) / 1000,
                'n_samples': f.samples.size,
                'twt': f.samples,
            }
            # Load trace headers
            self.trace_header = self.parse_trace_headers(f)

    def parse_trace_headers(self, segyfile):
        # Get all header keys
        headers = segyio.tracefield.keys
        # Initialize dataframe with trace id as index and headers as columns
        df = pd.DataFrame(index=range(1, self.stats['n_traces'] + 1),
                          columns=headers.keys())
        # Fill dataframe with all header values
        for k, v in headers.items():
            df[k] = segyfile.attributes(v)[:]
        return df

    def parse_text_header(self, segyfile):
        '''
        Format segy text header into a readable, clean dict
        '''
        raw_header = segyio.tools.wrap(segyfile.text[0])
        # Cut on C*int pattern
        cut_header = re.split(r'C[\d|\s]\d\s', raw_header)[1::]
        # Remove end of line return
        text_header = [x.replace('\n', ' ') for x in cut_header]
        text_header[-1] = text_header[-1][:-2]
        # Format in dict
        clean_header = {}
        i = 1
        for item in text_header:
            key = "C" + str(i).rjust(2, '0')
            i += 1
            clean_header[key] = item
        return clean_header

    def export_text_header(self, output='root'):
        # Resolve output filename
        filename = self.stats['filename']
        if output == 'root':
            out = filename.parent
        else:
            out = filename.parent.joinpath('Text headers')
            out.mkdir(parents=True, exist_ok=True)
        # Save image
        outfile = out.joinpath(f'{filename.stem}_text_header.txt')
        # Write to file
        f = open(outfile, 'w')
        for k, v in self.text_header.items():
            f.write(f'{k} - {v}\n')
        f.close()
        print('Text header exported')

    def export_bin_header(self, output='root'):
        # Resolve output filename
        filename = self.stats['filename']
        if output == 'root':
            out = filename.parent
        else:
            out = filename.parent.joinpath('Bin headers')
            out.mkdir(parents=True, exist_ok=True)
        # Save image
        outfile = out.joinpath(f'{filename.stem}_bin_header.txt')
        # Write to file
        f = open(outfile, 'w')
        for k, v in self.bin_header.items():
            f.write(f'{k} - {v}\n')
        f.close()
        print('Bin header exported')

    def export_trace_header(self, output='root'):
        # Resolve output filename
        filename = self.stats['filename']
        if output == 'root':
            out = filename.parent
        else:
            out = filename.parent.joinpath('Trace headers')
            out.mkdir(parents=True, exist_ok=True)
        # Save image
        outfile = out.joinpath(f'{filename.stem}_trace_header.txt')
        # Write to file
        self.trace_header.to_csv(outfile)
        print('Trace header exported')


class Seis_navmerge(Segy):

    def __init__(self):
        pass


class Seis_shot(Segy):

    def __init__(self):
        pass


class Seis_section(Segy):

    def __init__(self):
        pass


def import_section(filename, data=True):
    segy = Seis_section()
    segy.load(filename, data)
    return segy

def import_navmerge(filename, data=False):
    segy = Seis_navmerge()
    segy.load(filename, data)
    return segy
