import numpy as np
import segyio
import vmlib as vm


def _get_outfilename(file, output_type, folder, suffix):
    filename = file.stats['filename']
    if output_type == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath(folder)
        out.mkdir(parents=True, exist_ok=True)
    return out.joinpath(f'{filename.stem}_{suffix}.jpg')


def _get_outfolder(file, folder):
    out = file.stats['filename'].parent.joinpath(folder)
    out.mkdir(parents=True, exist_ok=True)
    return out


def basemap(file, output='root', src=True, rcv=True, cdp=True, midpoints=True):
    outfile = _get_outfilename(file, output, 'Maps', 'basemap')
    vm.plot.seis.basemap_line(file, outfile, src, rcv, cdp, midpoints)
    vm.utils.print.info('Basemap created', 3)
    return outfile


def elevation(file, output='root'):
    outfile = _get_outfilename(file, output, 'Elevations', 'elevation')
    vm.plot.seis.elevation(file, outfile)
    vm.utils.print.info('Elevation created', 3)
    return outfile


def offset_cdp_fold(file, output='root'):
    outfile = _get_outfilename(file, output, 'Fold', 'cdp_offset_fold')
    vm.plot.seis.offset_cdp_fold(file, outfile)
    vm.utils.print.info('CDP-Offset-Fold chart created', 3)
    return outfile


def amplitude_offset(file, output='root'):
    outfile = _get_outfilename(file, output, 'Amplitude', 'amplitude_offset')
    vm.plot.seis.amplitude_offset(file, outfile)
    vm.utils.print.info('Amplitude-Offset chart created', 3)
    return outfile


def stacking(file, output='root'):
    outfile = _get_outfilename(file, output, 'Geometry', 'shooting_geometry')
    vm.plot.seis.stacking(file, outfile)
    vm.utils.print.info('Stacking chart created', 3)
    return outfile


def fold(file, output='root'):
    outfile = _get_outfilename(file, output, 'Fold', 'fold')
    vm.plot.seis.fold(file, outfile)
    vm.utils.print.info('Fold chart created', 3)
    return outfile


def cdp_spacing(file, output='root'):
    outfile = _get_outfilename(file, output, 'Spacing', 'cdp_spacing')
    vm.plot.seis.cdp_spacing(file, outfile)
    vm.utils.print.info('CDP spacing chart created', 3)
    return outfile


def rms_map(file, output='root'):
    outfile = _get_outfilename(file, output, 'RMS_Maps', 'rms_map')
    vm.plot.seis.rms_map(file, outfile)
    vm.utils.print.info('RMS Map created', 3)
    return outfile


def gathers_short(file, par):
    # General parameters
    out_folder = _get_outfolder(file, 'Shot Gathers')
    twt = [t for t in file.stats['twt'] if t <= par['short_offset_cut']]
    # Get list of all FFIDs and create dict
    ffids = file.trace_header['FieldRecord'].unique()
    shots = {k:{'src': 0, 'data': [], 'offsets': [], 'rcvs': [], 'twt': twt} for k in ffids}
    # Open file and loop on each trace
    with segyio.open(file.stats['filename'], ignore_geometry=True) as f:
        for ix, trace in enumerate(f.trace):
            off = file.traces.data.loc[ix+1, 'offset']
            if abs(off) <= par['short_offset_lim']:
                tr_ffid = file.trace_header.loc[ix + 1, 'FieldRecord']
                src = file.traces.data.loc[ix+1, 'src_station']
                rcv = file.traces.data.loc[ix+1, 'rcv_station']
                shots[tr_ffid]['src'] = src
                shots[tr_ffid]['data'].append(trace[:len(twt)].copy())
                shots[tr_ffid]['offsets'].append(off)
                shots[tr_ffid]['rcvs'].append(rcv)
    # Format to np.array
    for ffid in shots.keys():
        shots[ffid]['data'] = np.stack(t for t in shots[ffid]['data'])
    # Send to plotting
    vm.plot.seis.short_gathers(file, shots, out_folder, par)

    vm.utils.print.info('Gathers files created', 3)
    return out_folder
