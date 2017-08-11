import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import colorsys
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
import matplotlib


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    red = int(round(red))
    green = int(round(green))
    blue = int(round(blue))
    return '#%02x%02x%02x' % (red, green, blue)

def hls_to_hex(hue, lightness, saturation):
    rgb_val = np.array(colorsys.hls_to_rgb(hue, lightness, saturation))*255
    return rgb_to_hex(*rgb_val)

def hex_to_hls(hex_val):
    rgb_val = np.array(hex_to_rgb(hex_val))/255.0
    return np.array(colorsys.rgb_to_hls(*rgb_val))

def colors(i, lightness=None):
    """get color index i with desired lightness"""
    hls_val = hex_to_hls(current_palette[i])
    if lightness != None:
        hls_val[1] = lightness 
    new_hex = hls_to_hex(*hls_val)
    return new_hex

#          red        blue        green       purple   orange     brown        pink      gray       

blue = lambda lightness=None: colors(0,lightness)
orange = lambda lightness=None: colors(1,lightness)
green = lambda lightness=None: colors(2,lightness)
red = lambda lightness=None: colors(3,lightness)
purple = lambda lightness=None: colors(4,lightness)
brown = lambda lightness=None: colors(5,lightness)
pink = lambda lightness=None: colors(6,lightness)
gray = lambda lightness=None: colors(7,lightness)

def set_colors_list(colors):
    """set current color cycle to colors (list)"""
    global current_palette
    current_palette = colors
    mpl.rcParams.update({'axes.prop_cycle': mpl.cycler('color', colors)})

def set_colors(palette):
    """set current color cycle to existing pallete"""
    set_colors_list(color_palettes[palette])


color_palettes = {
    "main" : ["#0066ff", rgb_to_hex(255,127,14), "#89a02c", "#ff0000", "#7b2b8b", "#a05a2c", "#ff55dd", "#4d4d4d"],

    "main soft" : ["#377eb8", "#ff7f00", "#4daf4a", "#e41a1c", "#984ea3", "#a65628" , "#f781bf", "#666666"],

    "norbert" : ["#0000ff", "#ff7f2a", "#89a02c", "#ff0000", "#800080", "#a05a2c", "#ff55dd", "#222222"],

    "mpl2": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],

    "palette1" : ["#066fba", "#d74c11","#ecaf1c", "#7b2b8b", "#72a92a", "#d40000", "#0000ff", "#6c5353"],

    "color blind" : [rgb_to_hex(0,0,0),
               rgb_to_hex(230,159,0),
               rgb_to_hex(86,180,233),
               rgb_to_hex(0,158,115),
               rgb_to_hex(240,228,66),
               rgb_to_hex(0,114,178),
               rgb_to_hex(213,94,0),
               rgb_to_hex(204,121,167)],
    }

default_palette = color_palettes['main']
current_palette = default_palette
set_colors_list(default_palette)


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    """return a truncated colormap from an existing one
            cmap        color map
            minval      lower bound
            maxval      upper bound
            n           number of values """
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

# colormaps

parula_data = [[0.2081, 0.1663, 0.5292], [0.2116238095, 0.1897809524, 0.5776761905], 
 [0.212252381, 0.2137714286, 0.6269714286], [0.2081, 0.2386, 0.6770857143], 
 [0.1959047619, 0.2644571429, 0.7279], [0.1707285714, 0.2919380952, 
  0.779247619], [0.1252714286, 0.3242428571, 0.8302714286], 
 [0.0591333333, 0.3598333333, 0.8683333333], [0.0116952381, 0.3875095238, 
  0.8819571429], [0.0059571429, 0.4086142857, 0.8828428571], 
 [0.0165142857, 0.4266, 0.8786333333], [0.032852381, 0.4430428571, 
  0.8719571429], [0.0498142857, 0.4585714286, 0.8640571429], 
 [0.0629333333, 0.4736904762, 0.8554380952], [0.0722666667, 0.4886666667, 
  0.8467], [0.0779428571, 0.5039857143, 0.8383714286], 
 [0.079347619, 0.5200238095, 0.8311809524], [0.0749428571, 0.5375428571, 
  0.8262714286], [0.0640571429, 0.5569857143, 0.8239571429], 
 [0.0487714286, 0.5772238095, 0.8228285714], [0.0343428571, 0.5965809524, 
  0.819852381], [0.0265, 0.6137, 0.8135], [0.0238904762, 0.6286619048, 
  0.8037619048], [0.0230904762, 0.6417857143, 0.7912666667], 
 [0.0227714286, 0.6534857143, 0.7767571429], [0.0266619048, 0.6641952381, 
  0.7607190476], [0.0383714286, 0.6742714286, 0.743552381], 
 [0.0589714286, 0.6837571429, 0.7253857143], 
 [0.0843, 0.6928333333, 0.7061666667], [0.1132952381, 0.7015, 0.6858571429], 
 [0.1452714286, 0.7097571429, 0.6646285714], [0.1801333333, 0.7176571429, 
  0.6424333333], [0.2178285714, 0.7250428571, 0.6192619048], 
 [0.2586428571, 0.7317142857, 0.5954285714], [0.3021714286, 0.7376047619, 
  0.5711857143], [0.3481666667, 0.7424333333, 0.5472666667], 
 [0.3952571429, 0.7459, 0.5244428571], [0.4420095238, 0.7480809524, 
  0.5033142857], [0.4871238095, 0.7490619048, 0.4839761905], 
 [0.5300285714, 0.7491142857, 0.4661142857], [0.5708571429, 0.7485190476, 
  0.4493904762], [0.609852381, 0.7473142857, 0.4336857143], 
 [0.6473, 0.7456, 0.4188], [0.6834190476, 0.7434761905, 0.4044333333], 
 [0.7184095238, 0.7411333333, 0.3904761905], 
 [0.7524857143, 0.7384, 0.3768142857], [0.7858428571, 0.7355666667, 
  0.3632714286], [0.8185047619, 0.7327333333, 0.3497904762], 
 [0.8506571429, 0.7299, 0.3360285714], [0.8824333333, 0.7274333333, 0.3217], 
 [0.9139333333, 0.7257857143, 0.3062761905], [0.9449571429, 0.7261142857, 
  0.2886428571], [0.9738952381, 0.7313952381, 0.266647619], 
 [0.9937714286, 0.7454571429, 0.240347619], [0.9990428571, 0.7653142857, 
  0.2164142857], [0.9955333333, 0.7860571429, 0.196652381], 
 [0.988, 0.8066, 0.1793666667], [0.9788571429, 0.8271428571, 0.1633142857], 
 [0.9697, 0.8481380952, 0.147452381], [0.9625857143, 0.8705142857, 0.1309], 
 [0.9588714286, 0.8949, 0.1132428571], [0.9598238095, 0.9218333333, 
  0.0948380952], [0.9661, 0.9514428571, 0.0755333333], 
 [0.9763, 0.9831, 0.0538]]

def phase_cmap(): 
    """ Return a black-white scale phase color map"""
    white = '#ffffff'
    black = '#000000'
    red = '#ff0000'
    blue = '#0000ff'
    anglemap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'anglemap', [black, white, black], N=256, gamma=1)
    return anglemap


cmap = {'parula': LinearSegmentedColormap.from_list('parula', parula_data),
        'viridis_short': truncate_colormap(mpl.cm.viridis, maxval=0.92),
        'phase': phase_cmap()}




class colored_line:
    def __init__(self, x, y, c, **kwargs):
        """Small wrapper for a LineCollection with easier to use set_data functions
               x[N]                   xdata
               y[N]                   ydata
               c[N], c[N,3], c[N,4]   color data
               **kwargs               kwargs valid for matplotlib.LineCollection
        """
        x = np.asarray(x)
        y = np.asarray(y)
        c = np.asarray(c)

        xy = np.vstack([x,y]).T
        xy = xy.reshape(-1, 1, 2)
        segments = np.hstack([xy[:-1], xy[1:]])

        self.collection = LineCollection(segments, **kwargs)
        self.collection.set_edgecolor(c)

    def set_data(self, x, y, c=None):
        """Set new x and y data, optionally new color data
               x[N]                   xdata
               y[N]                   ydata
               c[N], c[N,3], c[N,4]   color data (default: current colors)
        """

        xy = np.vstack([x,y]).T
        xy = xy.reshape(-1, 1, 2)
        segments = np.hstack([xy[:-1], xy[1:]])

        self.collection.set_segments(segments)
        if c is not None:
            self.collection.set_edgecolor(c)
        
    def set_xdata(self, x):
        """Set new x (must be same size as current y data)
               x[N]                   xdata
        """
        segments = np.array(self.collection.get_segments())
        segments[:,0,0] = x[:-1]
        segments[:,1,0] = x[1:]
        self.collection.set_segments(segments)

    def set_ydata(self, y):
        """Set new y (must be same size as current x data)
               y[N]                   ydata
        """
        segments = np.array(self.collection.get_segments())
        segments[:,0,1] = y[:-1]
        segments[:,1,1] = y[1:]
        self.collection.set_segments(segments)

    def set_colors(self, c):
        """Set new color data
               c[N], c[N,3], c[N,4]   color data
        """
        self.collection.set_edgecolor(c)

def colored_plot(x, y, c, ax=None, **kwargs):
    """Like matplotlib plot, but use a list of colors c for variable color. Return a colored_line
            x[N]                   xdata
            y[N]                   ydata
            c[N], c[N,3], c[N,4]   color data
            ax                     axis (default: current axis)
            **kwargs               kwargs valid for matplotlib.LineCollection
    """
    if ax is None:
        ax = plt.gca()
    line = colored_line(x,y,c, **kwargs)

    ax.add_collection(line.collection)
    return line


