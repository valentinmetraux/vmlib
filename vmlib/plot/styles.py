# -*- coding: utf-8 -*-

# Copyright: V.Métraux
# Version: 06.03.2019
# Author: V.Métraux

'''
Objects for dealing with graphics and plotting needs

This module provides many objects to deal with graphics tasks.
All functions are based on matplotlib library.

Parameter functions
-------------------
- 'textParameter'     - Update matplotlib text parameters
- 'lineParameter'     - Update matplotlib line parameters
- 'layoutParameter'   - Update matplotlib figure parameters
- 'axisParameter'     - Update matplotlib axis parameters
- 'gridParameter'     - Update matplotlib grid parameters
- 'legendParameter'   - Update matplotlib legend parameters
- 'saveParameter'     - Update matplotlib save parameters
- 'graphParameter'    - Update matplotlib graph parameters
'''
import matplotlib as mpl


def set_plot_styles(text=[True, 10],
                    line=True, layout=True,
                    axis=[True, ''], grid=True, legend=True,
                    save=[True, 300]):
    '''
    set_plot_styles(text, line, layout, axis, grid, legend, save)

    Update matplotlib graph parameters from user-specified needs

    Parameters
    ----------
    text: list([Display bool, size int])
    line: boolean, default value = True
    layout: boolean, default value = True
    axis: list([Display bool, spines str ('all', else)])
    grid: boolean, default value = True
    legend: boolean, default value = True
    save: list([Display bool, dpi int])

    Returns
    -------
    None

    Notes
    -----
    See http://matplotlib.sourceforge.net/users/customizing.html
    '''
    if save[0]:
        saveParameter(save[1])
    if text[0]:
        textParameter(text[1])
    if layout:
        layoutParameter()
    if grid:
        gridParameter()
    if legend:
        legendParameter()
    if line:
        lineParameter()
    if axis:
        axisParameter(axis[1])


def saveParameter(dpi):
    '''
    saveParameter()

    Update matplotlib graph save parameters from user-specified needs

    Parameters
    ----------
    dpi:    dpi int

    Returns
    -------
    None
    '''
    mpl.rcParams['savefig.dpi'] = dpi
    mpl.rcParams['savefig.pad_inches'] = 0.1
    mpl.rcParams['savefig.jpeg_quality'] = 95


def textParameter(size):
    '''
    textParameter()

    Update matplotlib graph text parameters from user-specified needs

    Parameters
    ----------
    size:   Base font size (in px)

    Returns
    -------
    None
    '''
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.style'] = 'normal'
    mpl.rcParams['font.variant'] = 'normal'
    mpl.rcParams['font.weight'] = 'normal'
    mpl.rcParams['font.stretch'] = 'normal'
    mpl.rcParams['font.size'] = size
    mpl.rcParams['font.serif'] = ['Times New Roman', 'Times', 'serif']
    mpl.rcParams['font.sans-serif'] = ['Lucida Grande', 'Verdana',
                                       'Arial', 'Helvetica', 'sans-serif']
    mpl.rcParams['figure.titlesize'] = 'x-large'
    mpl.rcParams['figure.titleweight'] = 'bold'
    mpl.rcParams['axes.titlesize'] = 'large'
    mpl.rcParams['axes.titleweight'] = 'bold'
    mpl.rcParams['axes.labelsize'] = 'medium'
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['xtick.labelsize'] = 'small'
    mpl.rcParams['ytick.labelsize'] = 'small'
    mpl.rcParams['legend.fontsize'] = 'small'


def lineParameter():
    '''
    lineParameter()

    Update matplotlib graph line parameters from user-specified needs

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    mpl.rcParams['lines.linewidth'] = 0.75
    mpl.rcParams['lines.linestyle'] = '-'
    mpl.rcParams['lines.color'] = 'E24A33'
    mpl.rcParams['lines.marker'] = None
    mpl.rcParams['lines.markeredgewidth'] = 0.5
    mpl.rcParams['lines.markersize'] = 2
    mpl.rcParams['lines.markerfacecolor'] = 'auto'
    mpl.rcParams['lines.markeredgecolor'] = 'auto'
    mpl.rcParams['lines.dash_joinstyle'] = 'round'
    mpl.rcParams['lines.dash_capstyle'] = 'butt'
    mpl.rcParams['lines.dashed_pattern'] = [6, 6]
    mpl.rcParams['lines.dashdot_pattern'] = [3, 5, 1, 5]
    mpl.rcParams['lines.dotted_pattern'] = [1, 3]
    mpl.rcParams['lines.solid_joinstyle'] = 'round'
    mpl.rcParams['lines.solid_capstyle'] = 'projecting'
    mpl.rcParams['lines.antialiased'] = True
    mpl.rcParams['markers.fillstyle'] = 'full'
    mpl.rcParams['patch.linewidth'] = 0.25
    mpl.rcParams['patch.facecolor'] = '348ABD'
    mpl.rcParams['patch.force_edgecolor'] = True
    mpl.rcParams['patch.edgecolor'] = 'EEEEEE'
    mpl.rcParams['patch.antialiased'] = True
    mpl.rcParams['hist.bins'] = 15
    mpl.rcParams['hatch.color'] = 'black'
    mpl.rcParams['hatch.linewidth'] = 0.15
    mpl.rcParams['image.aspect'] = 'equal'
    mpl.rcParams['image.interpolation'] = 'bilinear'
    mpl.rcParams['image.cmap'] = 'viridis'
    mpl.rcParams['image.lut'] = 256
    mpl.rcParams['image.origin'] = 'upper'
    mpl.rcParams['image.resample'] = False
    mpl.rcParams['image.composite_image'] = True
    mpl.rcParams['contour.negative_linestyle'] = 'dashed'
    mpl.rcParams['contour.corner_mask'] = True
    mpl.rcParams['errorbar.capsize'] = 3
    mpl.rcParams['scatter.marker'] = 'o'
    mpl.rcParams['boxplot.bootstrap'] = None
    mpl.rcParams['boxplot.boxprops.color'] = 'black'
    mpl.rcParams['boxplot.boxprops.linestyle'] = '-'
    mpl.rcParams['boxplot.boxprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.capprops.color'] = 'black'
    mpl.rcParams['boxplot.capprops.linestyle'] = '-'
    mpl.rcParams['boxplot.capprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.flierprops.color'] = 'black'
    mpl.rcParams['boxplot.flierprops.linestyle'] = 'none'
    mpl.rcParams['boxplot.flierprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.flierprops.marker'] = '+'
    mpl.rcParams['boxplot.flierprops.markeredgecolor'] = 'black'
    mpl.rcParams['boxplot.flierprops.markerfacecolor'] = 'auto'
    mpl.rcParams['boxplot.flierprops.markersize'] = 6.0
    mpl.rcParams['boxplot.meanline'] = False
    mpl.rcParams['boxplot.meanprops.color'] = 'red'
    mpl.rcParams['boxplot.meanprops.linestyle'] = '-'
    mpl.rcParams['boxplot.meanprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.medianprops.color'] = 'red'
    mpl.rcParams['boxplot.meanprops.marker'] = 's'
    mpl.rcParams['boxplot.meanprops.markerfacecolor'] = 'red'
    mpl.rcParams['boxplot.meanprops.markeredgecolor'] = 'black'
    mpl.rcParams['boxplot.meanprops.markersize'] = 6.0
    mpl.rcParams['boxplot.medianprops.linestyle'] = '-'
    mpl.rcParams['boxplot.medianprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.notch'] = False
    mpl.rcParams['boxplot.patchartist'] = False
    mpl.rcParams['boxplot.showbox'] = True
    mpl.rcParams['boxplot.showcaps'] = True
    mpl.rcParams['boxplot.showfliers'] = True
    mpl.rcParams['boxplot.showmeans'] = False
    mpl.rcParams['boxplot.vertical'] = True
    mpl.rcParams['boxplot.whiskerprops.color'] = 'black'
    mpl.rcParams['boxplot.whiskerprops.linestyle'] = '--'
    mpl.rcParams['boxplot.whiskerprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.whiskers'] = 1.5


def layoutParameter():
    '''
    layoutParameter()

    Update matplotlib graph layout parameters from user-specified needs

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    mpl.rcParams['figure.dpi'] = 80
    mpl.rcParams['figure.facecolor'] = 'white'
    mpl.rcParams['figure.subplot.left'] = 0.10
    mpl.rcParams['figure.subplot.right'] = 0.90
    mpl.rcParams['figure.subplot.top'] = 0.90
    mpl.rcParams['figure.subplot.bottom'] = 0.10
    mpl.rcParams['figure.subplot.wspace'] = 0.15
    mpl.rcParams['figure.subplot.hspace'] = 0.15
    mpl.rcParams['figure.figsize'] = [8, 6]
    mpl.rcParams['figure.edgecolor'] = 'gray'
    mpl.rcParams['figure.autolayout'] = False
    mpl.rcParams['figure.frameon'] = True


def axisParameter(spines):
    '''
    axisParameter()

    Update matplotlib graph axis parameters from user-specified needs

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    mpl.rcParams['axes.axisbelow'] = True
    mpl.rcParams['axes.facecolor'] = 'E5E5E5'
    mpl.rcParams['axes.edgecolor'] = '444444'
    mpl.rcParams['axes.linewidth'] = 0.75
    mpl.rcParams['axes.titlepad'] = 15.0
    mpl.rcParams['axes.labelpad'] = 5.0
    mpl.rcParams['axes.labelcolor'] = 'black'
    mpl.rcParams['axes.formatter.limits'] = [-5, 5]
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler('color', ['#4878D0',
                                                           '#EE854A',
                                                           '#6ACC64',
                                                           '#D65F5F',
                                                           '#956CB4',
                                                           '#8C613C',
                                                           '#DC7EC0',
                                                           '#797979',
                                                           '#D5BB67',
                                                           '#82C6E2'])
    mpl.rcParams['axes.autolimit_mode'] = 'round_numbers'
    mpl.rcParams['axes.xmargin'] = 0.05
    mpl.rcParams['axes.ymargin'] = 0.05
    mpl.rcParams['axes.spines.bottom'] = True
    mpl.rcParams['axes.spines.left'] = True
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False
    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['xtick.major.size'] = 4
    mpl.rcParams['xtick.minor.size'] = 2
    mpl.rcParams['xtick.minor.visible'] = True
    mpl.rcParams['xtick.major.width'] = 0.5
    mpl.rcParams['xtick.minor.width'] = 0.25
    mpl.rcParams['xtick.major.pad'] = 4
    mpl.rcParams['xtick.minor.pad'] = 4
    mpl.rcParams['xtick.color'] = '444444'
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['xtick.major.top'] = False
    mpl.rcParams['xtick.major.bottom'] = True
    mpl.rcParams['xtick.minor.top'] = False
    mpl.rcParams['xtick.minor.bottom'] = True
    mpl.rcParams['xtick.alignment'] = 'center'
    mpl.rcParams['ytick.left'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['ytick.major.size'] = 4
    mpl.rcParams['ytick.minor.size'] = 2
    mpl.rcParams['ytick.minor.visible'] = True
    mpl.rcParams['ytick.major.width'] = 0.5
    mpl.rcParams['ytick.minor.width'] = 0.25
    mpl.rcParams['ytick.major.pad'] = 4
    mpl.rcParams['ytick.minor.pad'] = 4
    mpl.rcParams['ytick.color'] = '444444'
    mpl.rcParams['ytick.direction'] = 'out'
    mpl.rcParams['ytick.major.left'] = True
    mpl.rcParams['ytick.major.right'] = False
    mpl.rcParams['ytick.minor.left'] = True
    mpl.rcParams['ytick.minor.right'] = False
    mpl.rcParams['ytick.alignment'] = 'center'
    if spines == 'all':
        mpl.rcParams['axes.spines.right'] = True
        mpl.rcParams['axes.spines.top'] = True
        mpl.rcParams['xtick.top'] = True
        mpl.rcParams['ytick.right'] = True
        mpl.rcParams['xtick.major.top'] = True
        mpl.rcParams['xtick.minor.top'] = True
        mpl.rcParams['ytick.major.right'] = True
        mpl.rcParams['ytick.minor.right'] = True


def gridParameter():
    '''
    gridParameter()

    Update matplotlib graph grid parameters from user-specified needs

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    mpl.rcParams['axes.grid'] = True
    mpl.rcParams['axes.grid.which'] = 'major'
    mpl.rcParams['axes.grid.axis'] = 'both'
    mpl.rcParams['grid.color'] = 'white'
    mpl.rcParams['grid.linestyle'] = '-'
    mpl.rcParams['grid.linewidth'] = 0.75
    mpl.rcParams['grid.alpha'] = 1.0


def legendParameter():
    '''
    legendParameter()

    Update matplotlib graph legend parameters from user-specified needs

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    mpl.rcParams['legend.fancybox'] = False
    mpl.rcParams['legend.loc'] = 'upper right'
    mpl.rcParams['legend.shadow'] = False
    mpl.rcParams['legend.handletextpad'] = 0.1
    mpl.rcParams['legend.borderaxespad'] = 1
    mpl.rcParams['legend.numpoints'] = 3
    mpl.rcParams['legend.borderpad'] = 0.4
    mpl.rcParams['legend.markerscale'] = 1.0
    mpl.rcParams['legend.labelspacing'] = 0.5
    mpl.rcParams['legend.handlelength'] = 2.0
    mpl.rcParams['legend.handleheight'] = 0.7
    mpl.rcParams['legend.columnspacing'] = 2.0
    mpl.rcParams['legend.frameon'] = True
    mpl.rcParams['legend.framealpha'] = None
    mpl.rcParams['legend.scatterpoints'] = 3
    mpl.rcParams['legend.facecolor'] = 'white'
    mpl.rcParams['legend.edgecolor'] = 'black'
