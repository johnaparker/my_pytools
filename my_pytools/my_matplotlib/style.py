import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from .plots import modify_legend
import colorsys
from mpl_toolkits.axes_grid1 import make_axes_locatable


palette1 = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628" , "#f781bf", "#666666"]

palette2 = ["#066fba", "#d74c11","#ecaf1c", "#7b2b8b", "#72a92a", "#d40000", "#0000ff", "#6c5353"]

palette3 = ["#ff0000", "#0000ff", "#89a02c", "#800080", "#ff7f2a", "#a05a2c", "#ff55dd", "#000000"]

main_colors = palette1

class figsize:
    def __init__(self, width, ratio = 0.8):
        """figure width and aspect ratio"""
        self.width = width
        self.ratio = ratio
        self.height = ratio*width

    def get(self):
        """return figsize as (width,height)"""
        return np.array((self.width, self.height))

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
    hls_val = hex_to_hls(main_colors[i])
    if lightness != None:
        hls_val[1] = lightness 
    new_hex = hls_to_hex(*hls_val)
    return new_hex

#          red        blue        green       purple   orange     brown        pink      gray       

red = lambda lightness=None: colors(0,lightness)
blue = lambda lightness=None: colors(1,lightness)
green = lambda lightness=None: colors(2,lightness)
purple = lambda lightness=None: colors(3,lightness)
orange = lambda lightness=None: colors(4,lightness)
brown = lambda lightness=None: colors(5,lightness)
pink = lambda lightness=None: colors(6,lightness)
gray = lambda lightness=None: colors(7,lightness)

def set_colors(colors):
    """set default color cycle to colors (list)"""
    main_colors = colors
    mpl.rcParams.update({'axes.prop_cycle': mpl.cycler('color', colors)})

def default(fontsize=16):
    """default settings"""
    mpl.rc('font', size=fontsize, family="Arial")
    mpl.rc('lines', linewidth=2, solid_capstyle="round")
    mpl.rc('axes', axisbelow=True, titlesize=fontsize, labelsize=fontsize)
    mpl.rc('legend', frameon=False, fontsize=fontsize)
    # mpl.rc('xtick', direction="out", labelsize=fontsize)
    # mpl.rc('ytick', direction="out", labelsize=fontsize)
    mpl.rc('figure', facecolor='white')
    mpl.rc('grid', linestyle='-', color='0.5')
    set_colors(palette1)
    # mpl.rcParams.update({"text.usetex": True})

def paper(fontsize=7):
    """paper settings"""
    default(fontsize)
    mpl.rc('lines', linewidth=1.5)
    mpl.rc('axes', linewidth=0.5)
    mpl.rcParams.update({'xtick.major.size': 2.0, 'ytick.major.size': 2.0})

    size = figsize(2)
    mpl.rc('figure', figsize=size.get())

    return size

def screen(fontsize=25):
    """screen settings"""
    default(fontsize)
    mpl.rc('lines', linewidth=3)
    mpl.rc('axes', linewidth=1.5)
    mpl.rcParams.update({'xtick.major.size': 7.0, 'ytick.major.size': 7.0})
    
    size = figsize(12)
    mpl.rc('figure', figsize=size.get())

    return size

def latex():
    """enable latex for all string expressions.
       By default, uses Helvetica font            """

    mpl.rcParams['text.usetex'] = True #Let TeX do the typsetting

    mpl.rcParams['font.family'] = 'sans-serif' # ... for regular text
    mpl.rcParams['font.sans-serif'] = 'Helvetica' # Choose a nice font here

    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}', r'\usepackage{physics}',  r'\usepackage[detect-all]{siunitx}', r'\sisetup{detect-all}',  r'\usepackage{upgreek}',
r'\renewcommand\familydefault\sfdefault',
r'\usepackage[symbolgreek,upright]{mathastext}',
r'\renewcommand\familydefault\rmdefault']

def remove_ticks():
    """remove x,y ticks, major and minor"""
    plt.gca().xaxis.set_ticks_position('none') 
    plt.gca().yaxis.set_ticks_position('none') 

def despine():
    """remove top-x and y-right axes"""
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    plt.gca().yaxis.set_ticks_position('left')
    plt.gca().xaxis.set_ticks_position('bottom')

def tighten():
    """tighen x,y labels and ticks"""
    plt.gca().tick_params(axis='both', which='major', pad=2)
    plt.gca().xaxis.labelpad = 1
    plt.gca().yaxis.labelpad = 0
    modify_legend(labelspacing=0.25)

def remove_frame():
    """remove all borders"""
    plt.gca().set_frame_on(False)

def axis_equal():
    """set the x,y axes length equal"""
    plt.gca().set_aspect('equal', adjustable='box')

def colorbar(im):
    """add a properly scaled colorbar"""
    ax = plt.gca()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cb = plt.colorbar(im,cax=cax )
    cb.ax.yaxis.set_tick_params(pad=1)

    return cb

def scientific_axis():
    """make y axis scientific"""
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))


# def presentation_sea(fontsize=16):
    # import seaborn as sns
    # sns.set_palette(sns.color_palette(colors))
    # sns.set_style("white")
    # sns.set_context("notebook", font_scale=fontsize/11.0, rc={"lines.linewidth": 2.0})
    # sns.set_style({'font.family': "Arial", 'text.color': "black", 'axes.labelcolor': '0.0',
        # 'xtick.color': '0.0', 'ytick.color': '0.0'})
