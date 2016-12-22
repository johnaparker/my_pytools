import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from .plots import modify_legend
from .colors import color_palettes
import colorsys
from mpl_toolkits.axes_grid1 import make_axes_locatable


class figsize:
    def __init__(self, width, ratio = 0.8):
        """figure width and aspect ratio"""
        self.width = width
        self.ratio = ratio
        self.height = ratio*width

    def get(self):
        """return figsize as (width,height)"""
        return np.array((self.width, self.height))

def default(fontsize=16):
    """default settings"""
    mpl.rc('font', size=fontsize, family="Arial")
    mpl.rc('lines', linewidth=2, solid_capstyle="round")
    mpl.rc('axes', axisbelow=True, titlesize=fontsize, labelsize=fontsize)
    mpl.rc('legend', frameon=False, fontsize=fontsize)
    mpl.rc('xtick', direction="out", labelsize=fontsize)
    mpl.rc('ytick', direction="out", labelsize=fontsize)
    mpl.rc('figure', facecolor='white')
    mpl.rc('grid', linestyle='-', color='0.5')


def paper(cols=1, fontsize=7):
    """paper settings"""
    default(fontsize)
    mpl.rc('lines', linewidth=1.0)
    mpl.rc('axes', linewidth=0.5)
    mpl.rcParams.update({'xtick.major.size': 2.0, 'ytick.major.size': 2.0})
    mpl.rcParams.update({'xtick.major.width': 0.5, 'ytick.major.width': 0.5})

    widths = {3: 2, 2: 3, 1: 4}

    size = figsize(widths[cols])
    mpl.rc('figure', figsize=size.get())

    return size

def screen(fontsize=25):
    """screen settings"""
    default(fontsize)
    mpl.rc('lines', linewidth=3)
    mpl.rc('axes', linewidth=1.5)
    mpl.rcParams.update({'xtick.major.size': 7.0, 'ytick.major.size': 7.0})
    mpl.rcParams.update({'xtick.major.width': 1.5, 'ytick.major.width': 1.5})
    
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
    half_ticks()

def half_ticks():
    """Only show ticks on the left and bottom spines"""
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

def fill_error_bar(x, lower, upper, color, alpha=0.35, linewidth=mpl.rcParams['lines.linewidth']/2.0):
    """error bar using fill in between lower and upper"""
    plt.fill_between(x, lower, upper, color=color, alpha=alpha,linewidth=linewidth)


# def presentation_sea(fontsize=16):
    # import seaborn as sns
    # sns.set_palette(sns.color_palette(colors))
    # sns.set_style("white")
    # sns.set_context("notebook", font_scale=fontsize/11.0, rc={"lines.linewidth": 2.0})
    # sns.set_style({'font.family': "Arial", 'text.color': "black", 'axes.labelcolor': '0.0',
        # 'xtick.color': '0.0', 'ytick.color': '0.0'})
