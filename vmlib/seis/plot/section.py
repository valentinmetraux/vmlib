# -*- coding: utf-8 -*-
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import segyio
import vmlib as vm


def section(s, outpath=None):

    # Additional args
        # Cut time
        # Colormap
        # Clip value
        # Orientation (from s.info)
        # Section type (time vs depth)
        # Display attribute (None, fold, etc...)
        # Display headers
        # Display spectra


    # Load data
    with segyio.open(s.info['file'], ignore_geometry=True) as f:
        data = f.trace.raw[:]
    # Reset styles and apply vmlib ones
    plt.style.use('ggplot')
    vm.plot.styles.set_plot_styles()
    # Create figure
    fig = plt.figure(figsize=(18, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Define clip and extent
    clip = np.percentile(data, 99)
    extent = [1, s.info['n_traces'],
              s.info['twt'][-1], s.info['twt'][0]]  # define extent
    # Plot and customize
    ax.imshow(data.T, cmap="RdBu", vmin=-clip, vmax=clip, aspect='auto',
              extent=extent)
    ax.set_xlabel('CDP number')
    ax.set_ylabel('TWT [ms]')
    ax.set_title(f"{s.info['file']}")



    if outpath is None:
        fig.show()
    else:
        filename = s.info['filename'].split('.')[0]
        out = pathlib.Path(outpath).joinpath(f'{filename}.jpg')
        fig.savefig(out)
