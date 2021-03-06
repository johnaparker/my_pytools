import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker
from matplotlib.ticker import MaxNLocator,MultipleLocator, FormatStrFormatter, FuncFormatter, ScalarFormatter
import matplotlib as mpl
from matplotlib import cm

def gradient_fill_between(x, y1, y2=0, values=None, cmap=None, where=None, ax=None):
    """
    Same as matplotlib fill_between but uses a colormap with values to color in the region
    """
    N  = len(x)
    dx = x[1] - x[0]

    if ax is None:
        ax = plt.gca()
    if np.isscalar(y1):
        y1 = np.full_like(x, y1)
    if np.isscalar(y2):
        y2 = np.full_like(x, y2)
    if where is None:
        where = np.full_like(x, True, dtype=bool)
    if values is None:
        values = np.linspace(0, 1, N)

    if cmap is None:
        cmap = mpl.cm.viridis
    elif isinstance(cmap, str):
        cmap = cm.get_cmap(cmap)

    verts = []
    for i in range(N-1):
        if where[i]:
            verts.append([(x[i],y1[i]), (x[i+1],y1[i+1]), (x[i+1],y2[i+1]), (x[i],y2[i]) ])

    colors = cmap(values)
    collection = mpl.collections.PolyCollection(verts, edgecolors=colors, facecolors=colors)
    ax.add_collection(collection)

def pcolor_z_info(data,xdata,ydata, ax=None):
    """ Allow pcolor data to be seen interactively in the plot
            data        2-d data
            xdata       1-d x data
            ydata       1-d y data
            ax          axis            """
    if not ax:
        ax = plt.gca()
    numrows, numcols = data.shape
    def format_coord(x, y):
        col = np.argmin(np.abs(x-xdata))
        row = np.argmin(np.abs(y-ydata))
        if col>=0 and col<numcols and row>=0 and row<numrows:
            z = data[row,col]
            return 'x=%1.4g, y=%1.4g, z=%1.4g'%(x, y, z)
        else:
            return 'x=%1.4g, y=%1.4g'%(x, y)

    ax.format_coord = format_coord
    return format_coord

def modify_legend(**kwargs):

    l = plt.gca().legend_
    if l == None:
        return

    defaults = dict(
        loc = l._loc,
        numpoints = l.numpoints,
        markerscale = l.markerscale,
        scatterpoints = l.scatterpoints,
        scatteryoffsets = l._scatteryoffsets,
        prop = l.prop,
        # fontsize = None,
        borderpad = l.borderpad,
        labelspacing = l.labelspacing,
        handlelength = l.handlelength,
        handleheight = l.handleheight,
        handletextpad = l.handletextpad,
        borderaxespad = l.borderaxespad,
        columnspacing = l.columnspacing,
        ncol = l._ncol,
        mode = l._mode,
        fancybox = type(l.legendPatch.get_boxstyle())==matplotlib.patches.BoxStyle.Round,
        shadow = l.shadow,
        title = l.get_title().get_text() if l._legend_title_box.get_visible() else None,
        framealpha = l.get_frame().get_alpha(),
        bbox_to_anchor = l.get_bbox_to_anchor()._bbox,
        bbox_transform = l.get_bbox_to_anchor()._transform,
        frameon = l._drawFrame,
        handler_map = l._custom_handler_map,
    )

    if "fontsize" in kwargs and "prop" not in kwargs:
        defaults["prop"].set_size(kwargs["fontsize"])

    defaults.update(kwargs)
    plt.legend(**defaults)


def fitted_colorbar(im, size="3%", pad=0.15, label=None, ax=None, **kwargs):
    """ Add a colorbar that matches the height of the figure
            im         the image (returned by pcolormesh/imshow)
            size       the width, as a percentatge ("x%")
            pad        spacing between figure and colorbar
            label      colorbar label        """
    if ax is None:
        ax = plt.gca()

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size=size, pad=pad)
    if label:
        cb = plt.colorbar(im,cax=cax, label=label, **kwargs)
    else:
        cb = plt.colorbar(im,cax=cax, **kwargs)

    return cb

def colorbar(cmap, vmin, vmax, label=None, **kwargs):
    """Adds a colorbar to the plot (useful when using colormaps outside of colormeshes)
            cmap         colormap
            vmin         minimum value
            vmax         maximum value
            label        colorbar label """

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cb = plt.colorbar(sm)   
    if label:
        cb.set_label(label, **kwargs)
    return cb

def top_colorbar(size="3%", pad=0.15, shrink=1.0, aspect=20, label=None, **colorbar_kw):
    """ Add a colorbar to the top of the figure
            size       the width, as a percentatge ("x%")
            pad        spacing between figure and colorbar
            label      colorbar label        """

    # divider = make_axes_locatable(plt.gca())
    # cax = divider.append_axes("top", size="5%", pad=0.05)
    cax,kw = mpl.colorbar.make_axes(plt.gca(), location='top', shrink=shrink, pad=pad, aspect=aspect)
    if label: kw['label'] = label
    kw.update(colorbar_kw)
    
    cb = plt.colorbar(cax=cax, format='%1.1f', **kw)
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')

    tick_locator = ticker.MaxNLocator(nbins=5)
    cb.locator = tick_locator
    cb.update_ticks()
    return cb


def scientific_axis(precision=1, power=None, ax=None, show_multiplier=True):
    """create a scientific_axis on the y-axis
            precision         floating point precision
            power             set the power value explicitly  
            ax                axis to be used
            show_multiplier   If true, draw the multiplier above the axis """

    if not ax:
        ax = plt.gca()

    # determine the power value
    if power == None:
        ymin, ymax = ax.get_ylim()
        # x = "%.{}e" % ymax 
        x = "{0:.{1}e}".format(ymax,precision)

        pos = x.find('+')
        sgn = ''
        if pos == -1:
            pos = x.find('-')
            sgn = '-'
        n = int(x[pos+1:])
        if sgn == '-':
            n *= -1
    else:
        n = power

    # set the formatter
    def formatter(xtick , pos):
        return '{0:.{1}f}'.format(xtick/10**n,precision)
    ax.yaxis.set_major_formatter( FuncFormatter(formatter) )

    # draw the multiplier
    if show_multiplier:
        bbox = ax.get_position()
        x,y = bbox.corners()[1]
        buff = bbox.height*0.01
        plt.figtext(x,y+buff, r'$\times \, \mathregular{{10^{{ {0} }} }}$'.format(n))
    # embed()

    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # plt.gca().yaxis.set_major_formatter( FormatStrFormatter('%.1f') )

def set_axis_formatter(format_str = '%.1f', axis='both'):
    if axis == 'both' or axis == 'x':
        plt.gca().xaxis.set_major_formatter( FormatStrFormatter(format_str) )
    if axis == 'both' or axis == 'y':
        plt.gca().yaxis.set_major_formatter( FormatStrFormatter(format_str) )

def set_num_ticks(min_ticks, max_ticks, axis='both', prune=None, ax=None):
    """ Set bounds on the number of ticks """
    if ax is None:
        ax = plt.gca()

    if axis == 'both' or axis == 'x':
        ax.xaxis.set_major_locator(MaxNLocator(min_n_ticks=min_ticks, nbins=max_ticks, prune=prune))
    if axis == 'both' or axis == 'y':
        ax.yaxis.set_major_locator(MaxNLocator(min_n_ticks=min_ticks, nbins=max_ticks, prune=prune))

def axis_equal_aspect(ax=None):
    """set axes aspect ratio to be equal"""
    if not ax:
        ax = plt.gca()
    x0,x1 = ax.get_xlim()
    y0,y1 = ax.get_ylim()
    ax.set_aspect((x1-x0)/(y1-y0))

