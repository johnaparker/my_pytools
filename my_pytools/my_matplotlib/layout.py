import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec


class alpha_labels:
    def __init__(self, loc = 2, outside=True, str_format='{0}', displacement=(0,0), color='black', capital=False, bold = True, eps = 0.01, bbox=None):
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

    def insert(self, ax = None, **kwargs):
        """Insert an alphanumeric label on axis ax (defaults to current). 
           Override text options with kwargs"""

        if not ax:
            ax = plt.gca()

        # get label and increment label counter
        label = self.str_format.format(chr(self.label_ord))
        self.label_ord += 1

        displace = self.rhat*self.eps + self.displacement

        # add text label
        dict_args = self.text_dict.copy()
        dict_args.update(kwargs)
        ax.text(self.xpos+displace[0],self.ypos+displace[1],label, transform=ax.transAxes, **dict_args)



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

