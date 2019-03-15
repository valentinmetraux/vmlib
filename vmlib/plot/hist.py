import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from . styles import set_plot_styles


def distribution(var=[], bins=20, title='', subtitle='',
                 xlabel='', ylabel='', out=''):
    # Reset styles and apply selected ones
    plt.style.use('classic')
    set_plot_styles()
    # Get variable statistics
    median = np.median(var)
    std = np.std(var)
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Plot histogram
    n, bins, patches = ax.hist(var, bins, density = True)
    # Plot best fit curve
    density = gaussian_kde(var)
    xs = np.linspace(min(var), max(var), 100)
    ax.plot(xs, density(xs), 'k--')
    # Add annotation
    string = f'Median: {median:.2f}\nStd dev.: {std:.2f}'
    ax.text(0.05, 0.95, string,
            horizontalalignment='left', verticalalignment='top',
            transform=ax.transAxes,
            bbox={'facecolor':'white', 'alpha':0.8, 'pad':5})
    # Fin tune
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(subtitle)
    fig.suptitle(title)
    fig.savefig(out)
    plt.close(fig)
