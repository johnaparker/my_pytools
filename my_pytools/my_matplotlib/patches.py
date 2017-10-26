# My patch objects

from matplotlib import patches,path
from matplotlib.collections import PatchCollection
import numpy as np
import matplotlib.pyplot as plt

def circle_arrow(center, radius, width, fraction, angle=0, reverse=False, ax=None, **kwargs):
    """A circular shaped arrow. Returns a PatchCollection

       Arguments:
           center      (x,y) center
           radius      radius of circle
           width       width of arrow head in data units
           fraction    fraction of arc to draw (0 to 1)
           angle       starting angle (default: 0)
           reverse    if True, place arrow head at start (default: False)
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

def bracket(p1, p2, height, text=None, drop_bracket=0, drop_text=0, ax=None, kw_bracket=None, kw_text=None):
    """Square bracket, including optional text
    
       Arguments:
           p1             top left corner
           p2             top right corner
           height         height of bracket
           text           text below the bracket (default: None)
           drop_bracket   distance to move the bracket down (default: 0)
           drop_text      distance to move the text down (default: 0)
           ax             axes (default: current axes)
           kw_bracket     optional kwargs for bracket object (patches.PathPatch)
           kw_text        optional kwargs for text object
    """
    if ax is None:
        ax = plt.gca()

    p1,p2 = map(np.asarray, [p1,p2])
    vertices = np.zeros([4,2])
    vertices[0] = p1
    vertices[1] = p1 - np.array([0,height])
    vertices[2] = p2 - np.array([0,height])
    vertices[3] = p2
    vertices[:,1] -= drop_bracket

    kwargs = {'color': 'black'}
    if kw_bracket is not None:
        kwargs.update(kw_bracket)
    bracket = patches.PathPatch(path.Path(vertices), fill=False, **kwargs)
    ax.add_patch(bracket)
    if text is not None:
        kwargs = {'color': 'black', 'verticalalignment': 'top', 'horizontalalignment': 'center'}
        if kw_bracket is not None:
            kwargs.update(kw_text)

        xpos = (vertices[1][0] + vertices[2][0])/2 
        ypos = vertices[1][1] - drop_text
        ax.text(xpos, ypos, text, **kwargs)

if __name__ == "__main__":
    plt.figure()

    arrow = circle_arrow((0,0), 0.5, width=.1, fraction=0.8, angle=.4*np.pi, reverse=False, lw=20, color='C0')

    plt.xlim([-1,1])
    plt.ylim([-1,1])
    plt.gca().set_aspect('equal')
    plt.show()

