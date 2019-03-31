import matplotlib.pyplot as plt
from . styles import set_plot_styles


def generic(var=[], aspect=False, title='', subtitle='',
            xlabel='', ylabel='', legend=True, out=''):
    # Reset styles and apply selected ones
    plt.style.use('ggplot')
    set_plot_styles()
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Plot all variables
    for v in var:
        ax.plot(v[0],v[1],label=v[2])
    # Set aspect
    if aspect:
        ax.set_aspect(aspect)
    # Legend
    if legend:
        ax.legend()
    # Fin tune
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(subtitle)
    fig.suptitle(title)
    fig.savefig(out)
    plt.close(fig)


def fill(x=[], y=[], aspect=False, title='', subtitle='', color='#6ACC64',
         xlabel='', ylabel='', legend=True, out=''):
    # Reset styles and apply selected ones
    plt.style.use('ggplot')
    set_plot_styles()
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    # Plot line
    ax.fill_between(x, y1=y, y2=0, alpha=0.6, color=color, linewidth=0.25)
    # Set aspect
    if aspect:
        ax.set_aspect(aspect)
    # Legend
    if legend:
        ax.legend()
    # Fin tune
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(subtitle)
    fig.suptitle(title)
    fig.savefig(out)
    plt.close(fig)
