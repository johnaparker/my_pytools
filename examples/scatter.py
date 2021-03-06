import numpy as np
import matplotlib.pyplot as plt
import my_pytools.my_matplotlib.style as style
import my_pytools.my_matplotlib.colors as colors
import matplotlib as mpl

style.screen()
colors.set_colors('mpl2')
# style.latex()

size = 2000
var = .8

x = np.random.normal(3,var, size=size)
y = np.random.normal(3,var, size=size)
plt.scatter(x,y, label='A1', alpha=0.5, s=20, rasterized=False)

x = np.random.normal(5,var, size=size)
y = np.random.normal(5,var, size=size)
plt.scatter(x,y, label='A1', alpha=0.5, s=20, rasterized=False)

x = np.random.normal(3,var, size=size)
y = np.random.normal(5,var, size=size)
plt.scatter(x,y, label='A1', alpha=0.5, s=20, rasterized=False)

x = np.random.normal(5,var, size=size)
y = np.random.normal(3,var, size=size)
plt.scatter(x,y, label='A1', alpha=0.5, s=20, rasterized=False)


x = np.random.normal(3+5,var, size=size)
y = np.random.normal(3,var, size=size)
plt.scatter(x,y, label='A1', alpha=0.5, s=20, rasterized=False)

x = np.random.normal(5+5,var, size=size)
y = np.random.normal(5,var, size=size)
plt.scatter(x,y, label='A1', alpha=0.5, s=20, rasterized=False)

x = np.random.normal(3+5,var, size=size)
y = np.random.normal(5,var, size=size)
plt.scatter(x,y, label='A1', alpha=0.5, s=20, rasterized=False)

x = np.random.normal(5+5,var, size=size)
y = np.random.normal(3,var, size=size)
plt.scatter(x,y, label='A1', alpha=0.5, s=20, rasterized=False)

plt.xlabel(r'acceleration ($\mu m/s^2$)')
plt.xlabel(r'acceleration $\left(\mu m/s^2 A \AA\right)$')
plt.ylabel(r'cross section $\left(\mu m^2 \right)$, $\sigma = 2.0$')

plt.text(1,0.4, r'$test$, $\sum_{n=0}^{n=10}{a_n \pi \lambda^2}$')
plt.text(8,0.4, r'$test$, $\mathregular{\sum_{n=0}^{n=10}{a_n \pi \lambda^2}}$')

plt.legend(frameon=True, framealpha=1)
# style.despine()
style.half_ticks()
plt.savefig('test.pdf')
plt.show()

