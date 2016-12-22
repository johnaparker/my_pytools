import numpy as np
import matplotlib.pyplot as plt
import my_pytools.my_matplotlib.style as style
import my_pytools.my_matplotlib.colors as colors
import my_pytools.my_matplotlib.plots as plots
import matplotlib

style.paper()
style.latex()
colors.set_colors("mpl2")

plt.figure(1)

x = np.linspace(-1,1,100)
for i in range(8):
    plt.plot(x,x+7-i, label= "plot {}".format(i))

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
style.fill_error_bar(x, x**2 -.3, x**2+.3, color=colors.red())
plt.plot(x,-x**2, color=colors.blue(), label='blue')
style.fill_error_bar(x, -x**2 -.3, -x**2+.3, color=colors.blue())

plt.plot(x,2*x, color=colors.green(), label=r'green')
style.fill_error_bar(x, 2*x -.3, 2*x+.3, color=colors.green())

plt.plot(x,-2*x, color=colors.orange(), label=r'orange')
style.fill_error_bar(x, -2*x -.3, -2*x +.3, color=colors.orange())

plt.ylabel(r"$\mathrm{m\alpha th}$, math")
plt.xlabel(r"Flux, neutrons $\left(\SI{}{\micro\meter^{-2}} \right)$")

plt.text(0,-1.8, r"$\mathrm{\displaystyle\sum_{n=0}^{n=10}{n^3}}$")
plt.text(0.0,2.0, r"$\mathrm{\bra{\psi}\ket{\psi}}$ $\expval{A}{\Psi}$")
plt.text(-0.6,-2.5, r"$\Omega = 2.0$")


# plots.modify_legend(edgecolor='white')
# plt.k
# plt.savefig("test.pdf", bbox_inches='tight')
style.half_ticks()
style.tighten()

leg = plt.legend(loc=2, frameon=True)
leg.get_frame().set_linewidth(0.5)
# plt.savefig("test.pdf")
plt.savefig("test.pdf", bbox_inches='tight', transparent=True)

plt.show()
