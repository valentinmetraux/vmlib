# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from scipy.ndimage import uniform_filter1d
from sklearn.preprocessing import robust_scale
from ..plot import hist, lines


def section(section='', timerange=[], tracerange=[],
            fold=True, cm='gray',
            hillshade=False, type='twt',
            hscale=5000, vscale=5000,
            output='root'):
    '''
    Display section
    '''
    # transpose data and get sample depths, fold
    data = section.data.T
    twt = section.stats['twt']
    fold_data = section.trace_header['NStackedTraces']
    # Check CDP orientation, reverse if cdp are reverse-ordered
    cdp_id = list(section.trace_header['CDP'])
    if cdp_id[0] > cdp_id[-1]:
        data = data[:, ::-1]
    # Cut time region
    if timerange != []:
        dd = (twt > timerange[0]) & (twt < timerange[1])
        data = data[dd, :]
        twt = twt[dd]
    # Cut trace region
    ntraces = np.shape(data)[1]
    cdp_range = range(0, ntraces)
    if tracerange != []:
        if tracerange[1] > np.shape(data)[1]:
            tracerange[1] = np.shape(data)[1]
        data = data[:, tracerange[0]:tracerange[1]]
        cdp_range = range(tracerange[0], tracerange[1])
        ntraces = len(cdp_range)
        fold_data = fold_data.iloc[tracerange[0] - 1:tracerange[1] - 1]
    # Get fold curve for relevant CDPs
    if fold:
        fold_x = list(fold_data.index)
        fold_y = list(fold_data.values)
    # Validate colormap
    if cm not in plt.colormaps():
        cm = 'gray'
    # Change labels if depth section
    if type != 'twt':
        ylabel = 'Depth under datum [m]'
    else:
        ylabel = 'Two-way time [ms]'
    # Compute figure dimensions

    # Adjust image dimension to hscale and vscale (adjust if twt or depth)
    figsize = (18, 10)

    # Initialize figure
    if fold:
        pass
        # SET PLOT STYLES

    else:
        fig, ax = plt.subplots(figsize=figsize)

    # Plot image
    if hillshade:
        # Create light source
        ls = mcolors.LightSource(0, 80)
        # Get color map
        cmap = plt.get_cmap(cm)
        # Normalize
        sc = robust_scale(data, axis=1,
                          with_centering=False,
                          with_scaling=True,
                          quantile_range=(0.2, 0.9),
                          )
        # Create HS
        hs = ls.hillshade(sc)
        size = int(50 / section.stats['sample_rate'])
        hs = uniform_filter1d(hs, size,
                              axis=0)
        hs = robust_scale(hs, axis=1,
                          with_centering=True,
                          with_scaling=False,
                          quantile_range=(0.01, 0.99),
                          )
        clip_val = abs(np.percentile(data, 0.999))
        ax.imshow(data, interpolation='bilinear',
                  aspect='auto', cmap=cm,
                  extent=(0, ntraces, twt[-1], twt[0]),
                  vmin=-clip_val, vmax=clip_val)
        ax.imshow(hs, cmap='binary', norm=None, aspect='auto',
                  interpolation=None, alpha=0.2, extent=(0, ntraces, twt[-1], twt[0]))
    else:
        clip_val = abs(np.percentile(data, 0.999))
        im = ax.imshow(data, interpolation='bilinear',
                       aspect='auto', cmap=cm,
                       extent=(0, ntraces, twt[-1], twt[0]),
                       vmin=-clip_val, vmax=clip_val)
    # Set tick number to CDP range
    n_ticks = 20
    round_to = 10
    x_step = int(round_to * round(float(ntraces / n_ticks) / round_to))
    # pixel count at label position
    x_positions = np.arange(0, ntraces, x_step)
    x_labels = cdp_range[::x_step]  # labels you want to see
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels)
    # Set labels
    ax.set_xlabel('CDP no.')
    ax.set_ylabel(ylabel)
    ax.set_title(section.stats['filename'])
    # Resolve output filename
    filename = section.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Sections')
        out.mkdir(parents=True, exist_ok=True)
    # Save image
    outfile = out.joinpath(f'{filename.stem}_section.jpg')
    fig.savefig(outfile)
    plt.close(fig)


def basemap(section='', output='root'):
    '''
    Plot CDPX-CDPY
    '''
    # Get scalar and compute cdp_x/y
    scalar = section.trace_header['SourceGroupScalar'].mean()
    if scalar < 0:
        cdp_x = list(section.trace_header['CDP_X'] / abs(scalar))
        cdp_y = list(section.trace_header['CDP_Y'] / abs(scalar))
    else:
        cdp_x = list(section.trace_header['CDP_X'])
        cdp_y = list(section.trace_header['CDP_Y'])
    # Resolve output filename
    filename = section.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Maps')
        out.mkdir(parents=True, exist_ok=True)
    # Plot and save
    lines.generic(var=[[cdp_x, cdp_y, 'CPD line']],
                  aspect=1,
                  title='CDP Map',
                  subtitle=filename,
                  xlabel='Easting [m]',
                  ylabel='Northing [m]',
                  legend=True,
                  out=out.joinpath(f'{filename.stem}_cdp_map.jpg'),
                  )


def cdp_spacing(section='', output='root'):
    '''
    Plot CDP spacing histogram
    '''
    # Get scalar and compute cdp_x/y
    scalar = section.trace_header['SourceGroupScalar'].mean()
    if scalar < 0:
        cdp_x = list(section.trace_header['CDP_X'] / abs(scalar))
        cdp_y = list(section.trace_header['CDP_Y'] / abs(scalar))
    else:
        cdp_x = list(section.trace_header['CDP_X'])
        cdp_y = list(section.trace_header['CDP_Y'])
    # Compute spacing
    dx = [(cdp_x[i] - cdp_x[i - 1]) for i in range(1, len(cdp_x))]
    dy = [(cdp_y[i] - cdp_y[i - 1]) for i in range(1, len(cdp_y))]
    spacing = [math.sqrt(dx[i]**2 + dy[i]**2) for i in range(len(dx))]
    # Resolve output filename
    filename = section.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Spacing')
        out.mkdir(parents=True, exist_ok=True)
    # Plot and save
    hist.distribution(var=spacing,
                      bins=20,
                      title='CDP spacing distribution',
                      subtitle=filename,
                      xlabel='CDP spacing [m]',
                      ylabel='Probability density',
                      out=out.joinpath(f'{filename.stem}_cdp_spacing.jpg'),
                      )


def distances(section='', inter_cdp=2.5, output='root'):
    '''
    Plot Cumulative versus Theoretical distances
    '''
    # Get scalar and compute cdp_x/y
    scalar = section.trace_header['SourceGroupScalar'].mean()
    if scalar < 0:
        cdp_x = list(section.trace_header['CDP_X'] / abs(scalar))
        cdp_y = list(section.trace_header['CDP_Y'] / abs(scalar))
    else:
        cdp_x = list(section.trace_header['CDP_X'])
        cdp_y = list(section.trace_header['CDP_Y'])
    # Compute spacing
    dx = [(cdp_x[i] - cdp_x[i - 1]) for i in range(1, len(cdp_x))]
    dy = [(cdp_y[i] - cdp_y[i - 1]) for i in range(1, len(cdp_y))]
    spacing = [math.sqrt(dx[i]**2 + dy[i]**2) for i in range(len(dx))]
    # Compute distances
    dist_cum = [sum(spacing[0:i]) for i in range(len(spacing))]
    dist_theo = [inter_cdp * (i) for i in range(len(spacing))]
    delta = [dist_cum[i] - dist_theo[i] for i in range(len(dist_cum))]
    # Resolve output filename
    filename = section.stats['filename']
    if output == 'root':
        out = filename.parent
    else:
        out = filename.parent.joinpath('Distances')
        out.mkdir(parents=True, exist_ok=True)
    # Plot and save
    lines.generic(var=[[range(len(delta)), delta, 'Delta']],
                  title='Distances (interCDP cumul. - theoretical cumul.)',
                  subtitle=filename,
                  xlabel='CPD Num.',
                  ylabel='Distance [m]',
                  legend=False,
                  out=out.joinpath(f'{filename.stem}_cdp_distances.jpg'),
                  )
