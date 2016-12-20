import numpy as np
import matplotlib.pyplot as plt
import my_pytools.my_matplotlib.style as style
import my_pytools.my_matplotlib.plots as plots
import matplotlib

figsize = style.screen()
style.latex()

plt.figure(1, figsize=figsize.get())

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
        color = style.hls_to_hex(main[j], lightness[i], .55)
        plt.plot(x,(i+1)*x + 4*j*x**2, marker=markers[i], color = color, markevery=10, markersize=9)
plt.grid()

plt.figure(3)
for i in np.linspace(0,3,15):
    plt.plot(x,(x+1)*i, color=style.red(.3 + i/3*.5), linewidth=4)

plt.figure(4)
# matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Arial']})
# matplotlib.rc('text', usetex=True)
# matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{cmbright}"]
# matplotlib.rcParams['mathtext.fontset'] = 'custom'
# matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
# matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
# matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'

plt.plot(x,x**2, color=style.red(), label='red')
plt.fill_between(x, x**2-.3, x**2+.3, color=style.red(), alpha=0.3, linewidth=0)
plt.plot(x,-x**2, color=style.blue(), label='blue')
plt.fill_between(x, -x**2-.5, -x**2+.5, color=style.blue(), alpha=0.3,linewidth=0)

plt.plot(x,2*x, color=style.green(), label=r'green')
plt.fill_between(x, 2*x-.3, 2*x+.3, color=style.green(), alpha=0.3,linewidth=0)

# plt.xlabel(r"$\mathrm{\lambda^2}$, $\lambda^2$, $\mathregular{\lambda^2}$, $m\alpha \boldsymbol{t}h$")
# plt.xlabel(r"$\mathrm{ m\alpha th}$")
plt.ylabel(r"$\mathrm{m\alpha th}$, math")
# plt.ylabel(r"$\mathrm{Flux, neutrons / cm^2}$")
# plt.ylabel(r"$\mathrm{Flux, neutrons \SI{20}{\micro\meter^2}$")
# plt.ylabel(r"$\mathrm{Flux, neutrons 20 \upmu m^2}$")
# plt.xlabel(r"Flux, neutrons $\left( \mathrm{\mu m^{-2}}\right)$")
plt.xlabel(r"Flux, neutrons $\left(\SI{}{\micro\meter^{-2}} \right)$")

plt.text(0,-1.8, r"$\mathrm{\displaystyle\sum_{n=0}^{n=10}{n^3}}$")
plt.text(0.0,2.0, r"$\mathrm{\bra{\psi}\ket{\psi}}$ $\expval{A}{\Psi}$")
plt.text(-0.6,-2.5, r"$\Omega = 2.0$")
# plt.title(r"$\Sigma$, $\mathrm{\Sigma}$, $\mathregular{\Sigma}$")

plt.legend(loc='best')
plt.savefig("test.pdf", bbox_inches='tight')
# plt.savefig("test.pdf")

plt.show()
