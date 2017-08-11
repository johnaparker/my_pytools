import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import colors
from my_pytools.my_matplotlib.colors import colored_plot

x = np.linspace(0,1,100)
y = np.linspace(0,1,100)
c = np.zeros((100,4))
c[:,0:3] = colors.to_rgb('C0')
c[:,3] = np.linspace(0,1,100)**1.5

line1 = colored_plot(x,y,c, linewidth=2, animated=True)
c[:,0:3] = colors.to_rgb('C1')
line2 = colored_plot(x,y,c, linewidth=2, animated=True)

def update(frame):
    t0 = 0.01*frame
    tf = t0 + 2*np.pi/3
    theta = np.linspace(t0, tf, 100)
    x = np.cos(theta)
    y = np.sin(theta)

    line1.set_data(x,y)

    theta  += np.pi
    x = np.cos(theta)
    y = np.sin(theta)
    line2.set_data(x,y)
    return [line1.collection,line2.collection]

plt.xlim([-1.5,1.5])
plt.ylim([-1.5,1.5])
plt.gca().set_aspect('equal')
anim = FuncAnimation(plt.gcf(), update, frames=np.arange(0,1000), repeat=True, interval=30, blit=True)
plt.show()

