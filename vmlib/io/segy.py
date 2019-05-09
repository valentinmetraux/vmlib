# -*- coding: utf-8 -*-
import re
import numpy as np
import pandas as pd
import segyio
import vmlib as vm


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
            # Load bin headers
            self.bin_header = f.bin
            # Load text headers
            self.text_header = self.parse_text_header(f)
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
        vm.utils.print.info('Text header', 3)

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
        vm.utils.print.info('Bin header', 3)

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
        vm.utils.print.info('Trace header', 3   )


class Seis_navmerge(Segy):

    def __init__(self):
        pass

    def clean_trace_headers(self):
        dropped = ['CDP_TRACE', 'NSummedTraces', 'SourceDepth',
                                'ReceiverDatumElevation',
                                'SourceDatumElevation', 'SourceWaterDepth',
                                'GroupWaterDepth', 'WeatheringVelocity',
                                'SubWeatheringVelocity', 'SourceUpholeTime',
                                'GroupUpholeTime', 'SourceStaticCorrection',
                                'GroupStaticCorrection', 'TotalStaticApplied',
                                'LagTimeA', 'LagTimeB', 'DelayRecordingTime',
                                'MuteTimeStart', 'MuteTimeEND',
                                'InstrumentGainConstant',
                                'InstrumentInitialGain', 'Correlated',
                                'SweepFrequencyStart', 'SweepFrequencyEnd',
                                'SweepLength', 'SweepType',
                                'SweepTraceTaperLengthStart',
                                'SweepTraceTaperLengthEnd', 'TaperType',
                                'AliasFilterFrequency', 'AliasFilterSlope',
                                'NotchFilterFrequency', 'NotchFilterSlope',
                                'LowCutFrequency', 'HighCutFrequency',
                                'LowCutSlope', 'HighCutSlope',
                                'TraceWeightingFactor',
                                'GeophoneGroupNumberRoll1',
                                'GeophoneGroupNumberFirstTraceOrigField',
                                'GeophoneGroupNumberLastTraceOrigField',
                                'GapSize', 'OverTravel', 'ShotPointScalar',
                                'TraceValueMeasurementUnit',
                                'TransductionConstantMantissa',
                                'TransductionConstantPower',
                                'TransductionUnit', 'TraceIdentifier',
                                'SourceType', 'SourceEnergyDirectionMantissa',
                                'SourceEnergyDirectionExponent',
                                'SourceMeasurementMantissa',
                                'SourceMeasurementExponent',
                                'SourceMeasurementUnit', 'UnassignedInt1',
                                'UnassignedInt2']
        self.trace_header.drop(dropped, axis=1, inplace=True)

    def get_receivers(self, header='CROSSLINE_3D'):
        # From traces headers, group on rcv_station
        groupings = {'ReceiverGroupElevation': 'mean',
                     'ElevationScalar': 'mean',
                     'GroupX': 'mean',
                     'GroupY': 'mean',
                     'SourceGroupScalar': 'mean'}
        df = self.trace_header.groupby(header).agg(groupings).copy()
        # Compute XYZ from raw and scalar
        df['x'] = df['GroupX'] / (-df['SourceGroupScalar'])
        df['y'] = df['GroupY'] / (-df['SourceGroupScalar'])
        df['z'] = df['ReceiverGroupElevation'] / (-df['ElevationScalar'])
        # Clean and format returned dataframe
        dropped = ['ReceiverGroupElevation', 'ElevationScalar', 'GroupX',
                   'GroupY', 'ElevationScalar', 'SourceGroupScalar']
        df.drop(dropped, axis=1, inplace=True)
        df.index.name = 'rcv_station'
        # Set as instance variable
        self.receivers = vm.seismic.rcv.RCV_line(df)
        vm.utils.print.info('RCV extracted', 3)
        return None

    def get_shots(self, src_between_rcv=True, rcv_header='CROSSLINE_3D',
                  src_header='ShotPoint'):
        # Group on FFID
        groupings = {'SourceSurfaceElevation': 'mean',
                     'ElevationScalar': 'mean',
                     'SourceX': 'mean',
                     'SourceY': 'mean',
                     'SourceGroupScalar': 'mean',
                     'EnergySourcePoint': 'mean',
                     src_header: 'mean',
                     'YearDataRecorded': 'mean',
                     'DayOfYear': 'mean',
                     'HourOfDay': 'mean',
                     'MinuteOfHour': 'mean',
                     'SecondOfMinute': 'mean'}
        df = self.trace_header.groupby('FieldRecord').agg(groupings).copy()
        # Compute XYZ from raw and scalar
        df['x'] = df['SourceX'] / (-df['SourceGroupScalar'])
        df['y'] = df['SourceY'] / (-df['SourceGroupScalar'])
        df['z'] = df['SourceSurfaceElevation'] / (-df['ElevationScalar'])
        # Format datetime of shoot from date / time headers
        df = df.rename(columns={'YearDataRecorded': 'year',
                                'DayOfYear': 'doy',
                                'HourOfDay': 'hour',
                                'MinuteOfHour': 'minute',
                                'SecondOfMinute': 'second',
                                'EnergySourcePoint': 'src_inline',
                                src_header: 'src_station'
                                })
        df['date'] = pd.to_datetime(df['year'],
                                    format='%Y') + pd.to_timedelta(df['doy']-1,
                                                                   unit='D')
        df['date'] += pd.to_timedelta(df['hour'], unit='H')
        df['date'] += pd.to_timedelta(df['minute'], unit='m')
        df['date'] += pd.to_timedelta(df['second'], unit='S')
        # Extract active stations
        df['first_rcv_station'] = self.trace_header.groupby('FieldRecord').agg({rcv_header: 'min'})
        df['last_rcv_station'] = self.trace_header.groupby('FieldRecord').agg({rcv_header: 'max'})
        df['n_traces'] = self.trace_header.groupby(['FieldRecord']).agg({'FieldRecord': 'count'})
        # Extract traces
        df['first_channel'] = self.trace_header.groupby('FieldRecord').agg({'TraceNumber': 'min'})
        df['last_channel'] = self.trace_header.groupby('FieldRecord').agg({'TraceNumber': 'max'})
        # If shot between rcv, then postfix 0.5
        if src_between_rcv:
            df['src_station'] += 0.5
        # Clean and format returned dataframe
        dropped = ['SourceSurfaceElevation', 'ElevationScalar', 'SourceX',
                   'SourceY', 'ElevationScalar', 'SourceGroupScalar', 'year',
                   'doy', 'hour', 'minute', 'second']
        df.drop(dropped, axis=1, inplace=True)
        df.index.name = 'ffid'
        # Set as instance variable
        self.shots = vm.seismic.src.SRC_line(df)
        vm.utils.print.info('SRC extracted', 3)
        return None

    def get_midpoints(self, src_between_rcv=True, rcv_header='CROSSLINE_3D',
                      src_header='ShotPoint'):
        # Create blank dataframe with index = trace sequence number
        df = pd.DataFrame(index=self.trace_header['TRACE_SEQUENCE_LINE'])
        # Get cdp id, x, y, offset
        df['src_station'] = self.trace_header[src_header]
        df['rcv_station'] = self.trace_header[rcv_header]
        if src_between_rcv:
            df['src_station'] += 0.5
        df['cdp_num'] = self.trace_header['CDP']
        df['cdp_x'] = self.trace_header['CDP_X'] / (-self.trace_header['SourceGroupScalar'])
        df['cdp_y'] = self.trace_header['CDP_Y'] / (-self.trace_header['SourceGroupScalar'])
        df['offset'] = self.trace_header['offset']
        # Get midpoint x, y
        df['src_x'] = self.trace_header['SourceX'] / (-self.trace_header['SourceGroupScalar'])
        df['src_y'] = self.trace_header['SourceY'] / (-self.trace_header['SourceGroupScalar'])
        df['rcv_x'] = self.trace_header['GroupX'] / (-self.trace_header['SourceGroupScalar'])
        df['rcv_y'] = self.trace_header['GroupY'] / (-self.trace_header['SourceGroupScalar'])
        df['x'] = 0.5*(df['src_x'] + df['rcv_x'])
        df['y'] = 0.5*(df['src_y'] + df['rcv_y'])
        df.drop(['src_x', 'src_y', 'rcv_x', 'rcv_y'], axis=1, inplace=True)
        # Compute CDP Fold

        def _get_fold(row, df):
            return np.in1d(df['cdp_num'].reset_index(drop=True),
                           row['cdp_num']).sum()

        df['fold'] = df.apply(lambda row: _get_fold(row, df), axis=1)
        # Set as instance variable
        self.midpoints = vm.seismic.cdp.CDP_line(df)
        vm.utils.print.info('Midpoints extracted', 3)
        return None

    def get_traces(self, header='CROSSLINE_3D', src_header='ShotPoint',
                   src_between_rcv=True):
        # Create blank dataframe with index = trace sequence number idem cdp
        df = pd.DataFrame(index=self.trace_header['TRACE_SEQUENCE_LINE'])
        # Get src and rcv id, channel number
        df['src_station'] = self.trace_header[src_header]
        df['rcv_station'] = self.trace_header[header]
        df['channel'] = self.trace_header['TraceNumber']
        if src_between_rcv:
            df['src_station'] += 0.5
        df['cdp_num'] = self.trace_header['CDP']
        df['offset'] = self.trace_header['offset']
        # Get trace code and keep valid
        df['trace_id_code'] = self.trace_header['TraceIdentificationCode']
        df = df[df['trace_id_code'] == 1] # Keep only valid seismic traces
        df.drop(['trace_id_code'], axis=1, inplace=True)
        # Get trace data
        with segyio.open(self.stats['filename'], ignore_geometry=True) as f:
            for ix, trace in enumerate(f.trace):
                df.loc[ix+1, 'amplitude'] = trace.max() - trace.min()
                df.loc[ix+1, 'rms'] = trace.std()
                df.loc[ix+1, 'rms_top'] = trace[:int(len(trace)/2)].std()
                df.loc[ix+1, 'rms_bkg'] = trace[int(len(trace)/2):-1].std()
        # Set as instance variable
        self.traces = vm.seismic.traces.Line(df)
        vm.utils.print.info('Traces extracted', 3)
        return None

    def get_attributes(self, epsg):
        # Search for LINE: entry in text_header
        for k, v in self.text_header.items():
            if 'LINE:' in v:
                line = v.split('LINE:')[1].split(' ')[1].strip()
                break
        # Format line num (integer) from line ID
        line_num = re.split("[,_\-:]+", line)[-1]
        line_num = int(re.sub("[^0-9]", "", line_num))
        # Store in instance variable as dict
        self.attributes = {
            'line': line,
            'line_num': line_num,
            'epsg': epsg,
        }

        vm.utils.print.info('Attributes extracted', 3)
        return None

    def generate_plots(self, par):
        vm.seismic.navmerge.basemap(self, par['output_type'], par['plot_src'],
                                    par['plot_rcv'], par['plot_cdp'],
                                    par['plot_midpoints'])
        vm.seismic.navmerge.elevation(self, par['output_type'])
        vm.seismic.navmerge.offset_cdp_fold(self, par['output_type'])
        vm.seismic.navmerge.stacking(self, par['output_type'])
        vm.seismic.navmerge.fold(self, par['output_type'])
        vm.seismic.navmerge.cdp_spacing(self, par['output_type'])
        if hasattr(self, 'traces'):
            vm.seismic.navmerge.amplitude_offset(self, par['output_type'])
            vm.seismic.navmerge.rms_map(self, par['output_type'])
            vm.seismic.navmerge.gathers_short(self, par)


            # Spectra (average, short & long offsets)
            # Export shots, offset classes, octave panels & CDP


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

def import_navmerge(filename, data=False, rcv_header='CROSSLINE_3D',
                    src_header='ShotPoint', src_between_rcv=True, epsg='2056'):
    navmerge = Seis_navmerge()
    navmerge.load(filename, data)
    # Get line attributes from headers
    navmerge.get_attributes(epsg)
    # Extract RCV, SRC and CDP
    navmerge.clean_trace_headers()
    navmerge.get_receivers(rcv_header)
    navmerge.get_shots(src_between_rcv, rcv_header, src_header)
    navmerge.get_midpoints(src_between_rcv, rcv_header, src_header)
    # Extract trace data if data extraction is validated
    if data:
        navmerge.get_traces(rcv_header, src_header, src_between_rcv)
    return navmerge
