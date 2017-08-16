"""Helper functions to perform animations"""

from itertools import cycle
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import animation
from my_pytools.my_matplotlib.geometry import rotation_transform
from my_pytools.my_matplotlib.colors import colored_plot
import matplotlib.patheffects as path_effects
from tqdm import tqdm

# Given X[N], Y[N,T], plot animated line
# Given f(x), f(y,t), plot animated line
# Repeat for X[Nx,Ny], etc, using pcolormesh or imshow and functional versions
    # included cmap/other controls for signed data vs unsigned
# For X,Y,U,V data, allow animated quiver

# possibly allow sprites, pcolormesh, and quiver animations to be overlapped easily

#TODO instead of full numpy arrays for raw data, use generators to compute on the fly

def save_animation(anim, filename, *args, **kwargs):
    """A wrapper for anim.save(...) that shows the progress of the saving

            anim        animation object
            filename    file output name
            *args       additional arguments to pass to anim.save
            **kwargs    additional keyword arguments to pass to anim.save
    """
    progress = tqdm(total = anim.save_count+1, ascii=True, desc="Saving video '{}'".format(filename))
    store_func = anim._func
    def wrapper(*args):
        progress.update()
        return store_func(*args)
    anim._func = wrapper
    anim.save(filename, *args, **kwargs)
    anim._func = store_func
    progress.close()

#TODO use matplotlib collections, patchcollection instead of python lists for performance
def trajectory_animation(coordinates, radii, projection, angles=None, colors=['C0'], ax=None,
        xlim=None, ylim=None, time=None, number_labels=False, trail=0, trail_type='normal',
        time_kwargs={}, label_kwargs={}, circle_kwargs={}, trail_kwargs={}, fading_kwargs={}):
    """create a 2D animation of trajectories

            coordinates[T,N,3]         particle x,y,z coordinates 
            radii[N]                   particle radii
            projection ('x','y','z')   which plane to project 3D trajectories onto
            angles[T,N]                particle angles
            colors                     list of colors to cycle through
            ax (default None)          specify the axes of the animation
            xlim[2]                    min,max values of x-axis
            ylim[2]                    min,max values of y-axis
            time[N]                    display the time (in microseconds)
            number_labels              include text labels (1,2,...) per particle
            trail                      length of particle trail
            trail_type                 'normal' or 'fading'
            time_kwargs                additional arguments to pass to timer text object
            label_kwargs               additional arguments to pass to label text objects
            circle_kwargs              additional arguments to circle properites
            trail_kwargs               additional arguments to line trail properies
            fading_kwargs              Fading line properites, {max_lw, min_lw}
    """
    trail_types = ['normal', 'fading']
    if trail_type not in trail_types:
        raise ValueError("trail_type '{}' is not valid. Choose from {}".format(trail_type, trail_types))
    if (trail_type == 'fading' and trail == np.inf):
        raise ValueError("trail cannot be fading and infinite")

    time_properties = dict(fontsize=12, zorder=2)
    time_properties.update(time_kwargs)

    label_properties = dict(horizontalalignment='center', verticalalignment='center', fontsize=14, zorder=2)
    label_properties.update(label_kwargs)

    trail_properties = dict(zorder=0)
    trail_properties.update(trail_kwargs)

    circle_properties = dict(facecolor=(1,1,1,0), linewidth=2, zorder=1)
    circle_properties.update(circle_kwargs)

    line_properties = deepcopy(circle_properties)
    line_properties.pop('facecolor')

    fading_properties = dict(max_lw=2, min_lw=0.3)
    fading_properties.update(fading_kwargs)

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

        circles.append(plt.Circle(coordinate, radii[i], edgecolor=color, animated=True, **circle_properties))
        ax.add_artist(circles[-1])

        if angles is not None:
            # lines.append(plt.Line2D([coordinate[0]-radii[i], coordinate[0]+radii[i]], [coordinate[1], coordinate[1]], lw=circle_properties['linewidth'], color=color, animated=True, zorder=circle_properties['zorder']))
            lines.append(plt.Line2D([coordinate[0]-radii[i], coordinate[0]+radii[i]], [coordinate[1], coordinate[1]], color=color, animated=True, **line_properties))
            ax.add_line(lines[-1])

        if trail > 0:
            if trail_type == 'normal':
                trails.append(ax.plot([coordinate[0]], [coordinate[1]], color=color, **trail_properties)[0])
            elif trail_type == 'fading':
                c = np.zeros((trail,4))
                c[:,0:3] = matplotlib.colors.to_rgb(color)
                c[:,3] = np.linspace(1,0,trail)
                lw = np.linspace(fading_properties['max_lw'],fading_properties['min_lw'],trail)
                trails.append(colored_plot([coordinate[0]], [coordinate[1]], c, ax=ax, linewidth=lw, **trail_properties))

        
        if number_labels:
            label = str(i+1)
            text[label] = ax.text(*coordinate, label, animated=True, **label_properties)
            text[label].set_path_effects([path_effects.Stroke(linewidth=5, foreground='white'),
                       path_effects.Normal()])

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    if time is not None:
        text['clock'] = ax.text(.98,0.02, r"{0:.2f} $\mu$s".format(0.0), transform=ax.transAxes, horizontalalignment='right', animated=True, **time_properties)

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
                trails[i].set_data(coordinates[t:tmin:-1,i,0], coordinates[t:tmin:-1,i,1])
            
            if number_labels:
                text[str(i+1)].set_position(coordinate + np.array([-radii[i], radii[i]]))
                # text[str(i+1)].set_position(coordinate)
                
        
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
    anim = trajectory_animation(coordinates, radii, 'z', colors=[f'C{i}' for i in range(10)], angles=angles, time = t, trail=30, number_labels=True, trail_type='fading')
    # anim.save('temp.mp4', dpi=150)
    plt.show()
