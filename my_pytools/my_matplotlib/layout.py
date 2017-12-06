import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


class alpha_labels:
    def __init__(self, loc = 2, outside=True, str_format='{0}', displacement=(0,0), color='black', capital=False, bold = True, eps = 0.01, bbox=None, **kwargs):
        """Create a new alphanumeric label class

                loc          corner anchor of the text (1,2,3,4)
                outside      if True, place text outside of axes
                str_format   format string for label
                displacment  additional displacement vector
                color        text color
                capital      if True, start with 'A'
                bold         if True, letters are bold
                eps          buffer between axes corner and text
                bbox         dictionary of values for background of text   """

        self.eps = eps
        self.displacement = np.asarray(displacement)
        self.label_ord = ord('A') if capital else ord('a')
        self.str_format = str_format

        verticalalignment = 'top' if (loc,outside) in ((1,False),(2,False),(3,True),(4,True)) else 'bottom'
        horizontalalignment = 'right' if (loc,outside) in ((1,False),(2,True),(3,True),(4,False)) else 'left'

        self.xpos = 1 if loc in (1,4) else 0
        self.ypos = 1 if loc in (1,2) else 0

        phi = np.pi*loc/2 - np.pi/4
        sgn = 1 if outside else -1 
        self.rhat = sgn*np.array([np.cos(phi), np.sin(phi)])

        self.text_dict = {'color': color, 'fontweight': 'normal', 'verticalalignment':verticalalignment, 'horizontalalignment':horizontalalignment, 'bbox':bbox}
        if bold == True: self.text_dict['fontweight'] = 'bold'
        self.text_dict.update(kwargs)

    def insert(self, ax = None, **kwargs):
        """Insert an alphanumeric label on axis ax (defaults to current). 
           Override text options with kwargs"""

        if not ax:
            ax = plt.gca()

        # get label and increment label counter
        label = self.str_format.format(chr(self.label_ord))
        self.label_ord += 1

        displace = self.rhat*self.eps + self.displacement

        width = ax.bbox.width
        height = ax.bbox.height

        # add text label
        dict_args = self.text_dict.copy()
        dict_args.update(kwargs)
        x = (self.xpos + displace[0])
        y = (self.ypos + displace[1])
        # x = x**(300/width)
        # y = y**(300/height)
        ax.text(x,y,label, transform=ax.transAxes, **dict_args)



class panels:
    def __init__(self, nrows, ncols=1, hspace = 0.1, wspace=0.1, width_ratios=None, height_ratios=None, left=0.1, top=0.9, right=0.9, bottom=0.1):
        """Create a grid of gridspecs for flexible figure layouts

                nrows                  number of rows
                ncols                  number of columns
                hspace                 gap space between rows
                wspace                 gap space between columns
                width_ratios[ncols]    relative ratios of column widths
                height_ratios[nrows]   relative ratios of row heights
                left                   figure left position
                top                    figure top position
                right                  figure right position
                bottom                 figure bottom position     """

        self.nrows = nrows
        self.ncols = ncols
        self.height = top - bottom
        self.width = right - left

        self.grid = np.zeros(shape=(nrows,ncols), dtype='O')

        self.hspace = hspace
        self.wspace = wspace

        if not width_ratios: width_ratios = np.ones(ncols)
        if not height_ratios: height_ratios = np.ones(nrows)
        self.width_panels = np.asarray(width_ratios)/np.sum(width_ratios)*(self.width - (ncols-1)*wspace)
        self.height_panels = np.asarray(height_ratios)/np.sum(height_ratios)*(self.height - (nrows-1)*hspace)

        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def add(self, gs_index, shape, hspace = 0.2, wspace=0.2, width_ratios=None, height_ratios=None, left_pad=0, right_pad=0, bottom_pad=0, top_pad=0):
        """Add a gridpec to the panel, and return it

                gs_index               (i,j) index of panel number; default j=0
                shape                  (nrows,ncols) for gridspec shape; default nrows=1
                hspace                 gap space between rows
                wspace                 gap space between columns
                width_ratios[ncols]    relative ratios of column widths
                height_ratios[nrows]   relative ratios of row heights
                left_pad               grispec left pad
                top_pad                gridpec top pad
                right_pad              gridpec right pad
                bottom_pad             gridpec bottom pad     """

        if not hasattr(gs_index, '__iter__'):
            gs_index = (gs_index,0)
        if not hasattr(shape, '__iter__'):
            shape = (1,shape)

        width = self.width_panels[gs_index[1]]
        height = self.height_panels[gs_index[0]]

        prev_width = np.sum(self.width_panels[:gs_index[1]])
        prev_height = np.sum(self.height_panels[:gs_index[0]])

        left = self.left + gs_index[1]*(self.wspace) + prev_width
        right = left + width
        top = self.top - gs_index[0]*(self.hspace) - prev_height
        bottom = top - height

        left += left_pad
        right -= right_pad
        bottom += bottom_pad
        top -= top_pad

        self.grid[gs_index] = gridspec.GridSpec(shape[0], shape[1], hspace=hspace, wspace=wspace, width_ratios=width_ratios, height_ratios=height_ratios, left=left, right=right, bottom=bottom, top=top)
        return self.grid[gs_index]

    def __index__(self):
        pass


def divide_gridspec(gs, index, gap=0, fig=None, gs1_size=None, gs2_size=None, gs1_widths=None, gs2_widths=None):
    """Divide a gridspec into 2 gridspecs along a vertical axis

            gs              gridpsec object
            index           number of figures left of the cut
            gap             distance added between two halves
            fig             figure object (defaults to current)
            gs1_size[2]     size of left gridspec (defaults to what was in gs)
            gs2_size[2]     size of right gridspec (defaults to what was in gs)
            gs1_widths[2]   width ratios of left gridspec (defaults to what was in gs)
            gs2_widths[2]   width ratios of right gridspec (defaults to what was in gs)

        Returns (gs_left, gs_right) """

    if not fig:
        fig = plt.gcf()

    nrow,ncol = gs.get_geometry()
    grid = gs.get_grid_positions(fig)
    
    # get the sizes and width ratios of 1,2
    size = gs.get_geometry()
    if not gs1_size:
        gs1_size = (size[0], index)
        gs1_widths = gs.get_width_ratios()[:index]
    if not gs2_size:
        gs2_size = (size[0], size[1] - index)
        gs2_widths = gs.get_width_ratios()[index:]

    # determine fraction of gap shifts needed to keep width ratios between 1 and 2 fixed
    # delta_1*gap is shift for left, delta_2*gap is shift for right
    widths = np.asarray(grid[3]) - np.asarray(grid[2])
    width_left = np.sum(widths[:index])
    width_right = np.sum(widths[index:])
    width_tot = np.sum(widths)
    delta_1 = width_left/width_tot
    delta_2 = width_right/width_tot

    # use grid to determine left,right,etc. positions
    bottom = grid[0][-1]
    top = grid[1][0]
    left_1 = grid[2][0]
    right_1 = grid[3][index-1]
    left_2 = grid[2][index]
    right_2 = grid[3][-1]

    gs1 = gridspec.GridSpec(gs1_size[0], gs1_size[1], left=left_1, bottom=bottom, top=top, right=right_1-gap*delta_1, width_ratios=gs1_widths)
    gs2 = gridspec.GridSpec(gs2_size[0], gs2_size[1], left=left_2+gap*delta_2, bottom=bottom, top=top, right=right_2, width_ratios=gs2_widths)

    return gs1,gs2


def get_axis_width_inches(ax):
    """Return the width of an axes in inches"""

    fig = ax.figure
    fig_width_inches = fig.bbox_inches.width
    fig_width_pixels = fig.bbox.width
    axis_width_pixels = ax.bbox.width

    axis_width_inches = axis_width_pixels/fig_width_pixels*fig_width_inches
    return axis_width_inches

def embed_anchored_axis(width, height=None, aspect_ratio=None, loc=1, pad=0.5, ax = None):
    """Add an embedded anchored axis to current axis. Returns the new axis

            width             new axis width (inches or "x%" of current ax width)
            height            new axis height (inches or "x%" of current ax width)
            aspect_ratio      if specified, set height based on heigh/width ratio
            loc               standard axis locator to anchor to
            pad               amount to pad between new axis and ax
            ax                axis (defualt to current)   """

    if not ax:
        ax = plt.gca()

    if not height and not aspect_ratio:
        raise ValueError("Either height or aspect_ratio must be given")

    if aspect_ratio:
        if type(width) == str:
            axes_width_inches = get_axis_width_inches(ax)
            frac = float(width.strip('%'))/100
            height = frac*axes_width_inches*aspect_ratio
        else:
            height = width*aspect_ratio

    new_ax = inset_axes(ax, width=width, height=height, loc=loc, borderpad=pad)

    return new_ax

def embed_anchored_image(img, width, loc=1, pad=0.1, ax=None):
    """Add an embedded anchored image to current axis. Returns (new_axis, dpi)
       where dpi is the dpi of the image in this axis

            width             new axis width (inches or "x%" of current ax width)
            loc               standard axis locator to anchor to
            pad               amount to pad between new axis and ax
            ax                axis (defualt to current)   """

    if not ax:
        ax = plt.gca()

    if type(width) == str:
        axis_width_inches = get_axis_width_inches(ax)

        frac = float(width.strip('%'))/100
        width = frac*axis_width_inches

    aspect_ratio = img.shape[0]/img.shape[1]
    new_ax = embed_anchored_axis(width=width, loc=loc, pad=pad, ax=ax, aspect_ratio=aspect_ratio)

    dpi = img.shape[1]/width
    return new_ax,dpi

def annotate(ax = None, arrow_props = None, **kwargs):
    """default annotate"""

    if not ax:
        ax = plt.gca()

    final_arrow_props = dict(arrowstyle='->', connectionstyle='arc3,rad=-0.3', linewidth=0.7, shrinkA=0, shrinkB=0)
    final_arrow_props.update(arrow_props)

    return ax.annotate(text, xy=xy, xy_text=xy_text, arrow_props=final_arrow_props, **kwargs)

### To be implemented
def axis_to_fig(width, height, ax = None):
    """convert axis point to figure point"""
    pass
    if not ax:
        ax = plt.gca()
    fig = ax.figure

def embed_axis():
    """embed axis at corner [xc,yc] with size [w,h]"""
    pass
def embed_image():
    """embed image at corner [xc,yc] with size [w,h]"""
    pass
    # x,y = ax.bbox.corners()[0]
    # w = ax.bbox.width
    # h = ax.bbox.height
    # x += w/2
    # y += h/2
    # W = fig.bbox.width
    # H = fig.bbox.height
    # fig.add_axes((x/W, y/H, w/W/2, h/H/2))
    # embed()

    # bbox_to_anchor=[1,2,3,4]
    # plt.axis('off')
    # img = np.fliplr(img)
    # plt.imshow(img)
