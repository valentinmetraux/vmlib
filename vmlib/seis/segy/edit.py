import pathlib
import scipy.signal as sps
import segyio


def cut(segy, cut_time=1000, outpath=pathlib.Path.cwd()):
    '''[summary]

    [description]

    Parameters
    ----------
    segy : {[type]}
        [description]
    cut_time : {number}, optional
        [description] (the default is 1000, which [default_description])
    outpath : {[type]}, optional
        [description] (the default is pathlib.Path.cwd(), which [default_description])

    Returns
    -------
    [type]
        [description]
    '''
    # Resolve destination file
    filename, extension = segy.info['filename'].split('.')
    destination = outpath.joinpath(f'{filename}_cut.{extension}')
    # Check cut-time and get final cut sample
    if cut_time > segy.info['trace_length']:
        cut_time = segy.info['trace_length']
    cut_sample = int(cut_time/segy.info['sample_rate'])
    # File opening and processing
    with segyio.open(segy.info['file'], ignore_geometry=True) as src:
        spec = segyio.tools.metadata(src)
        spec.samples = spec.samples[:cut_sample]
        with segyio.create(destination, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin = src.bin
            dst.bin.update(hns=len(spec.samples))
            dst.header = src.header
            dst.trace = src.trace
    return destination


def resample(segy, sample_rate=4, outpath=pathlib.Path.cwd()):
    '''Create a resample segy file (increase sampling rate)

    Creates a resampled segy file from an original segy. Note that the new
    sampling rate has to be a strict multiple of the original one.

    Parameters
    ----------
    segy : vmlib.seis.segy.io.Segy()
        instance of the source segyfile as loaded by vmlib.seis.segy.io
    sample_rate : float, optional
        destination sampling rate in milliseconds (defaults to 4 [ms])
    outpath : pathlib.Path, optional
        path to destination folder (defaults is pathlib.Path.cwd())

    Returns
    -------
    pathlib.Path
        path to the created, resampled, segy file

    Raises
    ------
    ValueError
        if the desired sample rate is not a strict multiple of the original one
    '''
    # Resolve destination file
    filename, extension = segy.info['filename'].split('.')
    destination = outpath.joinpath(f'{filename}_resample.{extension}')
    # Check new sampling rate
    if (sample_rate % segy.info['sample_rate']) == 0:
        ratio = int(sample_rate/segy.info['sample_rate'])
        # Process file
        with segyio.open(segy.info['file'], ignore_geometry=True) as src:
            spec = segyio.tools.metadata(src)
            spec.samples = spec.samples[:int(src.samples.size/ratio)-1]
            with segyio.create(destination, spec) as dst:
                dst.text[0] = src.text[0]
                dst.bin = src.bin
                for ix, trace in enumerate(src.trace):
                    dst.trace[ix] = sps.resample(trace,
                                                 int(len(trace)/ratio))
                dst.bin.update(hdt=sample_rate*1000)
                dst.bin.update(hns=len(spec.samples))
                dst.header = src.header
        return destination
    else:
        raise ValueError('Check sample rate to be multiple of the original')
