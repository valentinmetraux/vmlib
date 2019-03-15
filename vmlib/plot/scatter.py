import matplotlib.pyplot as plt
from . styles import set_plot_styles

def xy_map(x=[], y=[], title='Map', out=''):
    # Reset styles and apply selected ones
    plt.style.use('ggplot')
    set_plot_styles()
    # Plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(x, y)
    ax.set_xlabel('Easting [m]')
    ax.set_ylabel('Northing [m]')
    fig.suptitle(title)
    ax.set_aspect(1.0)
    fig.savefig(out)
    plt.close(fig)
