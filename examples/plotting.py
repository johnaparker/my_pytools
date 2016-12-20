import numpy as np
import matplotlib.pyplot as plt
import my_pytools.my_matplotlib.style as style
import my_pytools.my_matplotlib.colors as colors
import my_pytools.my_matplotlib.plots as plots
import matplotlib

style.screen()
style.latex()

plt.figure(1)

x = np.linspace(-1,1,100)
for i in range(8):
    plt.plot(x,x+7-i, label= "plot {}".format(i), linewidth=4)

plt.legend(loc=4, frameon=True)
plt.xlabel("My x label")
plt.ylabel("My y label")

# plots.remove_frame()
# style.despine()
# plt.grid()
# style.tighten()
# plt.tight_layout()
# plt.savefig("temp.pdf", transparent=True)

plt.figure(2)
N = 3
lightness = np.linspace(0.3, 0.70, N)
markers = ['o', 's', 'v']
main = [103/360, 207/360, 311/360]
for j in range(N):
    for i in range(3):
        color = colors.hls_to_hex(main[j], lightness[i], .55)
        plt.plot(x,(i+1)*x + 4*j*x**2, marker=markers[i], color = color, markevery=10, markersize=9)
plt.grid()

plt.figure(3)
for i in np.linspace(0,3,15):
    plt.plot(x,(x+1)*i, color=colors.red(.3 + i/3*.5), linewidth=4)

plt.figure(4)

plt.plot(x,x**2, color=colors.red(), label='red')
plt.fill_between(x, x**2-.3, x**2+.3, color=colors.red(), alpha=0.35, linewidth=2)
plt.plot(x,-x**2, color=colors.blue(), label='blue')
plt.fill_between(x, -x**2-.5, -x**2+.5, color=colors.blue(), alpha=0.35,linewidth=2)

plt.plot(x,2*x, color=colors.green(), label=r'green')
plt.fill_between(x, 2*x-.3, 2*x+.3, color=colors.green(), alpha=0.35,linewidth=2)

plt.plot(x,-2*x, color=colors.orange(), label=r'orange')
plt.fill_between(x, -2*x-.3, -2*x+.3, color=colors.orange(), alpha=0.35,linewidth=2)

plt.ylabel(r"$\mathrm{m\alpha th}$, math")
plt.xlabel(r"Flux, neutrons $\left(\SI{}{\micro\meter^{-2}} \right)$")

plt.text(0,-1.8, r"$\mathrm{\displaystyle\sum_{n=0}^{n=10}{n^3}}$")
plt.text(0.0,2.0, r"$\mathrm{\bra{\psi}\ket{\psi}}$ $\expval{A}{\Psi}$")
plt.text(-0.6,-2.5, r"$\Omega = 2.0$")

plt.legend(loc=2)
plt.savefig("test.pdf", bbox_inches='tight')

plt.show()
