import math
import matplotlib.pyplot as plt
import matplotlib as mpl
from . styles import set_plot_styles
from ..plot import hist


def basemap_line(file, outfile, src, rcv, cdp, midpoints):
    # Reset styles and apply vmlib ones
    plt.style.use('ggplot')
    set_plot_styles()
    # Create figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Plot variables
    if rcv:
        ax.plot(file.receivers.data['x'], file.receivers.data['y'], 'y-',
                label='Receivers')
    if src:
        ax.plot(file.shots.data['x'], file.shots.data['y'], 'r-',
                label='Shots')
    if cdp:
        # Remove duplicates and sort
        df = file.midpoints.data[['cdp_num', 'cdp_x', 'cdp_y']].copy()
        df.drop_duplicates(inplace=True)
        ax.plot(df['cdp_x'], df['cdp_y'], 'k-', label='CDP Line')
    if midpoints:
        x = file.midpoints.data['x']
        y = file.midpoints.data['y']
        z = abs(file.midpoints.data['offset'])
        cmap = mpl.cm.get_cmap('viridis')
        scat = ax.scatter(x, y, c=z, cmap=cmap, label='Midpoints',
                          s=0.5, alpha=0.8)
        fig.colorbar(scat, ax=ax, label='Absolute offset [m]', fraction=0.046,
                     pad=0.04)
    # Tuning labels and titles
    ax.set_xlabel('Easting [m]')
    ax.set_ylabel('Northing [m]')
    ax.set_aspect(1.0)
    ax.legend()
    ax.set_title(file.attributes['line'])
    fig.suptitle('Basemap')
    # Save
    fig.savefig(outfile)
    plt.close(fig)


def elevation(file, outfile):
    # Reset styles and apply vmlib ones
    plt.style.use('ggplot')
    set_plot_styles()
    # Create figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Plot variables
    ax.plot(file.receivers.data.index, file.receivers.data['z'], 'y-',
            label='Receivers')
    ax.plot(file.shots.data['src_station'], file.shots.data['z'], 'r-',
            label='Shots')
    # Tuning labels and titles
    ax.set_xlabel('Station')
    ax.set_ylabel('Elevation [m.a.s.l.]')
    ax.legend()
    ax.set_title(file.attributes['line'])
    fig.suptitle('Elevations')
    # Save
    fig.savefig(outfile)
    plt.close(fig)


def offset_cdp_fold(file, outfile):
    # Reset styles and apply vmlib ones
    plt.style.use('ggplot')
    set_plot_styles()
    # Create figure
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Plot variables
    x = file.midpoints.data['cdp_num']
    y = file.midpoints.data['offset']
    z = file.midpoints.data['fold']
    cmap = mpl.cm.get_cmap('viridis')
    scat = ax.scatter(x, y, c=z, cmap=cmap, s=1)
    fig.colorbar(scat, ax=ax, label='CDP Fold', fraction=0.046,
                 pad=0.04)
    # Tuning labels and titles
    ax.set_xlabel('CDP Number')
    ax.set_ylabel('Offset [m]')
    ax.set_title(file.attributes['line'])
    fig.suptitle('CDP vs Offset vs Fold crossplot')
    # Save
    fig.savefig(outfile)
    plt.close(fig)


def amplitude_offset(file, outfile):
    # Reset styles and apply vmlib ones
    plt.style.use('ggplot')
    set_plot_styles()
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Plot variables
    x = file.traces.data['offset']
    y = file.traces.data['max'] - file.traces.data['min']
    ax.scatter(x, y, s=1)
    ax.set_ylim([0, max(y)])
    # Tuning labels and titles
    ax.set_xlabel('Offset [m]')
    ax.set_ylabel('Amplitude range')
    ax.set_title(file.attributes['line'])
    fig.suptitle('Amplitude - Offset')
    # Save
    fig.savefig(outfile)
    plt.close(fig)


def stacking(file, outfile):
    # Reset styles and apply vmlib ones
    plt.style.use('ggplot')
    set_plot_styles()
    # Create figure
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Plot variables
    x = file.midpoints.data['rcv_station']
    y = file.midpoints.data['src_station']
    z = file.midpoints.data['offset']
    cmap = mpl.cm.get_cmap('viridis')
    scat = ax.scatter(x, y, c=z, cmap=cmap, s=1)
    fig.colorbar(scat, ax=ax, label='Offset [m]', fraction=0.046,
                 pad=0.04)
    # Tuning labels and titles
    ax.set_xlabel('RCV Station')
    ax.set_ylabel('SRC Station')
    ax.set_title(file.attributes['line'])
    fig.suptitle('Shooting geometry vs offset')
    # Save
    fig.savefig(outfile)
    plt.close(fig)


def fold(file, outfile):
    # Reset styles and apply vmlib ones
    plt.style.use('ggplot')
    set_plot_styles()
    # Create figure
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Plot variables
    # Remove duplicates and sort
    df = file.midpoints.data[['cdp_num', 'fold']].copy()
    df.drop_duplicates(inplace=True)
    x = df['cdp_num']
    y = df['fold']
    ax.fill_between(x, y1=y, y2=0, alpha=0.6, linewidth=0.25)
    ax.plot(x, y, '-k', linewidth=0.25)
    ax.set_xlim([0, max(x)])
    ax.set_ylim([0, max(y)+5])
    # Tuning labels and titles
    ax.set_xlabel('CDP number')
    ax.set_ylabel('Fold')
    ax.set_title(file.attributes['line'])
    fig.suptitle('CDP Fold')
    # Save
    fig.savefig(outfile)
    plt.close(fig)


def cdp_spacing(file, outfile):
    # Get CDP and drop duplicates
    df = file.midpoints.data[['cdp_num', 'cdp_x', 'cdp_y']].copy()
    df.drop_duplicates(inplace=True)
    cdp_x = list(df['cdp_x'])
    cdp_y = list(df['cdp_y'])
    # Compute spacing
    dx = [(cdp_x[i] - cdp_x[i - 1]) for i in range(1, len(cdp_x))]
    dy = [(cdp_y[i] - cdp_y[i - 1]) for i in range(1, len(cdp_y))]
    spacing = [math.sqrt(dx[i]**2 + dy[i]**2) for i in range(len(dx))]
    # Plot and save
    hist.distribution(var=spacing,
                      bins=20,
                      title='CDP spacing distribution',
                      subtitle=file.attributes['line'],
                      xlabel='CDP spacing [m]',
                      ylabel='Probability density',
                      out=outfile)
