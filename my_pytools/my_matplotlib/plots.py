import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker

def mkcmap(): 
    white = '#ffffff'
    black = '#000000'
    red = '#ff0000'
    blue = '#0000ff'
    anglemap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'anglemap', [black, red, white, blue, black], N=256, gamma=1)
    return anglemap

def pcolor_z_info(data,xdata,ydata, ax=None):
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



def fitted_colorbar(im, size="3%", pad=0.15, label=None):
    """ Add a colorbar that matches the height of the figure
            im         the image (returned by pcolormesh/imshow)
            size       the width, as a percentatge ("x%")
            pad        spacing between figure and colorbar
            label      colorbar label        """
    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", size=size, pad=pad)
    if label:
        cb = plt.colorbar(im,cax=cax, label=label)
    else:
        cb = plt.colorbar(im,cax=cax)

    return cb

def colorbar(cmap, vmin, vmax, label=None):
    """Adds a colorbar to the plot (useful when using colormaps outside of colormeshes)
            cmap         colormap
            vmin         minimum value
            vmax         maximum value
            label        colorbar label """

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cb = plt.colorbar(sm)   
    if label:
        cb.set_label(label)
    return cb

def top_colorbar(size="3%", pad=0.15, label=None):
    """ Add a colorbar to the top of the figure
            size       the width, as a percentatge ("x%")
            pad        spacing between figure and colorbar
            label      colorbar label        """

    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("top", size="5%", pad=0.05)
    cb = plt.colorbar(cax=cax, orientation='horizontal',label = "Angular scattering Intensity",format='%1.1f')
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')

    tick_locator = ticker.MaxNLocator(nbins=5)
    cb.locator = tick_locator
    cb.update_ticks()
    return cb

