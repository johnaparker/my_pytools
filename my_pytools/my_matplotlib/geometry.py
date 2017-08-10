"""Helper functions for 2d sprites"""

import matplotlib as mpl
import numpy as np

def rotation_transform(axis, angle, ax = None):
    """Return a rotation transfrom that rotates around an axis by an angle
            axix[2]       (x,y) center of rotation
            angle         angle of rotation (in degrees)  """

    if ax is None: ax = plt.gca()
    t_scale = ax.transData
    t_rotate = mpl.transforms.Affine2D().rotate_deg_around(axis[0], axis[1], angle*180/np.pi)
    return t_rotate + t_scale
