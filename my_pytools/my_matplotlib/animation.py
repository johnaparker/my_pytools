"""Helper functions to perform animations"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from matplotlib import animation
from my_pytools.my_matplotlib.geometry import rotation_transform
import matplotlib.patheffects as path_effects

# Given X[N], Y[N,T], plot animated line
# Given f(x), f(y,t), plot animated line
# Repeat for X[Nx,Ny], etc, using pcolormesh or imshow and functional versions
    # included cmap/other controls for signed data vs unsigned
# For X,Y,U,V data, allow animated quiver

# possibly allow sprites, pcolormesh, and quiver animations to be overlapped easily
#TODO instead of full numpy arrays for raw data, use generators to compute on the fly


#TODO use matplotlib collections, patchcollection instead of python lists for performance
#TODO include zorder
def trajectory_animation(coordinates, radii, projection, angles=None, ax=None, xlim=None, ylim=None,
        colors=['C0'], trail=0, time=None, number_labels=False):
    """create a 2D animation of trajectories
            coordinates[T,N,3]         particle x,y,z coordinates 
            radii[N]                   particle radii
            projection ('x','y','z')   which plane to project 3D trajectories onto
            angles[T,N]                particle angles
            ax (default None)          specify the axes of the animation
            xlim[2]                    min,max values of x-axis
            ylim[2]                    min,max values of y-axis
            colors                     list of colors to cycle through
            trail                      length of particle trail
            time[N]                    display the time (in microseconds)
            number_labels              include text labels (1,2,...) per particle
    """

    coordinates = np.asarray(coordinates)
    radii = np.asarray(radii)
    if angles is not None: 
        angles = np.asarray(angles)

    idx = [0,1,2]
    idx.pop(ord(projection) - ord('x'))
    coordinates = coordinates[...,idx]
    Nt,Nparticles,_ = coordinates.shape

    if ax is None:
        ax = plt.gca()
    if xlim is None:
        xlim = np.array([np.min(coordinates[...,0] - 1.3*radii),
                         np.max(coordinates[...,0] + 1.3*radii)])
    if ylim is None:
        ylim = np.array([np.min(coordinates[...,1] - 1.3*radii),
                         np.max(coordinates[...,1] + 1.3*radii)])
    color_cycle = cycle(colors)

    circles = []
    lines = []
    trails = []
    text = {}

    for i in range(Nparticles): 
        coordinate = coordinates[0,i]
        color = next(color_cycle)

        circles.append(plt.Circle(coordinate, radii[i], edgecolor=color, fc=(1,1,1,0), lw=2, animated=True, zorder=1))
        ax.add_artist(circles[-1])

        if angles is not None:
            lines.append(plt.Line2D([coordinate[0]-radii[i], coordinate[0]+radii[i]], [coordinate[1], coordinate[1]], lw=2, color=color, animated=True, zorder=2))
            ax.add_line(lines[-1])

        if trail > 0:
            trails.append(plt.plot([coordinate[0]], [coordinate[1]], color=color, zorder=0)[0])
        
        if number_labels:
            label = str(i+1)
            text[label] = ax.text(*coordinate, label,horizontalalignment='right', animated=True, fontsize=14)
            text[label].set_path_effects([path_effects.Stroke(linewidth=3, foreground='white'),
                       path_effects.Normal()])

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    if time is not None:
        text['clock'] = ax.text(.98,0.02, r"{0:.2f} $\mu$s".format(0.0), transform=ax.transAxes, horizontalalignment='right', fontsize=12, animated=True)

    def update(t):
        for i in range(Nparticles): 
            coordinate = coordinates[t,i]
            circles[i].center = coordinate

            if angles is not None:
                lines[i].set_data([coordinate[0]-radii[i], coordinate[0]+radii[i]], [coordinate[1], coordinate[1]])
                lines[i].set_transform(rotation_transform(coordinate, angles[t,i], ax=ax))

            if time is not None:
                text['clock'].set_text(r"{0:.2f} $\mu$s".format(t))

            if trail > 0:
                tmin = max(0,t-trail)
                trails[i].set_xdata(coordinates[tmin:t,i,0])
                trails[i].set_ydata(coordinates[tmin:t,i,1])
            
            if number_labels:
                text[str(i+1)].set_position(coordinate + np.array([-radii[i], radii[i]]))
                
        
        return  trails + circles + lines + list(text.values())

    anim = animation.FuncAnimation(ax.figure, update, frames=np.arange(0,Nt,1), interval=30, blit=True, repeat=True)
    return anim


if __name__ == "__main__":
    # plt.xkcd()
    N = 8
    Nt = 300
    t = np.linspace(0,100,Nt)
    coordinates = np.zeros([Nt, N, 3])
    angles = np.zeros([Nt,N])
    radii = np.ones(N)
    omega = .3

    for i in range(N):
        x = 3*np.cos(omega*t + 0.4*i)
        y = 2.5*i*np.ones_like(t) + 0.15*np.random.random(Nt)
        z = np.zeros_like(t)

        coordinates[:,i,:] = np.array([x,y,z]).T
        angles[:,i] = omega*t
    
    plt.figure()
    anim = trajectory_animation(coordinates, radii, 'z', colors=[f'C{i}' for i in range(10)], angles=angles, time = t, trail=np.inf, number_labels=True)
    # anim.save('temp.mp4', dpi=150)
    plt.show()
