import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from .plots import modify_legend

# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628" , "#f781bf"]
# colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
flatui_colors = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
ggplot_colors = ['E24A33', '348ABD', '988ED5', '777777', 'FBC15E', '8EBA42', 'FFB5B8']
main_colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628" , "#f781bf"]

class figsize:
    def __init__(self, width, ratio = 0.8):
        self.width = width
        self.ratio = ratio
        self.height = ratio*width

    def get(self):
        return np.array((self.width, self.height))

def set_colors(colors):
    mpl.rcParams.update({'axes.prop_cycle': mpl.cycler('color', colors)})

def default(fontsize=16):
    mpl.rc('font', size=fontsize, family="Arial")
    mpl.rc('lines', linewidth=2, solid_capstyle="round")
    mpl.rc('axes', axisbelow=True, titlesize=fontsize, labelsize=fontsize)
    mpl.rc('legend', frameon=False, fontsize=fontsize)
    # mpl.rc('xtick', direction="out", labelsize=fontsize)
    # mpl.rc('ytick', direction="out", labelsize=fontsize)
    mpl.rc('figure', facecolor='white')
    mpl.rc('grid', linestyle='-', color='0.8')
    set_colors(main_colors)
    # mpl.rcParams.update({"text.usetex": True})

def paper(fontsize=7):
    default(fontsize)
    mpl.rc('lines', linewidth=1.5)
    mpl.rcParams.update({'xtick.major.size': 2.5, 'ytick.major.size': 2.5})
    return figsize(2)

def screen(fontsize=22):
    default(fontsize)
    mpl.rc('lines', linewidth=3)
    return figsize(8)

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


# plt.rcParams['text.usetex'] = True #Let TeX do the typsetting
# plt.rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}',r'\sansmath']
#Force sans-serif math mode
# plt.rcParams['font.family'] = 'sans-serif' # ... for regular text
# plt.rcParams['font.sans-serif'] = 'Helvetica' # Choose a nice font here

# def presentation_sea(fontsize=16):
    # import seaborn as sns
    # sns.set_palette(sns.color_palette(colors))
    # sns.set_style("white")
    # sns.set_context("notebook", font_scale=fontsize/11.0, rc={"lines.linewidth": 2.0})
    # sns.set_style({'font.family': "Arial", 'text.color': "black", 'axes.labelcolor': '0.0',
        # 'xtick.color': '0.0', 'ytick.color': '0.0'})
