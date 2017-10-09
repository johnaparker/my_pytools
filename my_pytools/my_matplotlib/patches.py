# My patch objects

from matplotlib import patches
from matplotlib.collections import PatchCollection
import numpy as np

def circle_arrow(center, radius, width, fraction, angle=0, reverse=False, ax=None, **kwargs):
    """A circular shaped arrow. Returns a PatchCollection

       Arguments:
           center      (x,y) center
           radius      radius of circle
           width       width of arrow head in data units
           fraction    fraction of arc to draw (0 to 1)
           angle       starting angle (default: 0)
           reverese    if True, place arrow head at start (default: False)
           ax          axis to draw on (default: current axis)
           **kwargs    additional kwargs passed to Arc & Polygon
    """
    if ax is None:
        ax = plt.gca()
    theta = fraction*2*np.pi

    # line
    arc = patches.Arc(center, 2*radius, 2*radius, theta1=np.degrees(angle),
          theta2=np.degrees(theta + angle), capstyle='round', fill=False, **kwargs)

    # arrow head
    alpha = angle if reverse else angle + theta
    rotate = np.pi if reverse else 0

    px = center[0] + radius*np.cos(alpha)
    py = center[1] + radius*np.sin(alpha)
    head = patches.RegularPolygon(
            (px, py),            # center 
            3,                   # triangle shape
            width/3**0.5,        # radius
            alpha + rotate,      # orientation
            **kwargs,
           )

    arc.get_linewidth()
    ax.add_patch(arc)
    ax.add_patch(head)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    plt.figure()

    arrow = circle_arrow((0,0), 0.5, width=.1, fraction=0.8, angle=.4*np.pi, reverse=False, lw=20, color='C0')

    plt.xlim([-1,1])
    plt.ylim([-1,1])
    plt.gca().set_aspect('equal')
    plt.show()

