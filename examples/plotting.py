import numpy as np
import matplotlib.pyplot as plt
import my_pytools.my_matplotlib.style as style
import my_pytools.my_matplotlib.plots as plots
import matplotlib

figsize = style.screen()
plt.figure(1, figsize=figsize.get())

x = np.linspace(-1,1,100)

# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628" , "#f781bf"]
# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628" , "#f781bf"]
# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#ffbf00", "#984ea3", "#a65628" , "#f781bf"]
# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#ffbf00", "#984ea3", "#802b00" , "#f781bf"]
# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#ffbf00", "#9900cc", "#f781bf", "#00cccc", "#802b00"]
#          red        blue        green       orange   purple     pink       brown
#ff8000
# style.set_colors(colors)


for i in range(7):
    plt.plot(x,x+i, label= "plot {}".format(i), linewidth=4)

plt.legend(loc='best')
plt.xlabel("My x label")
plt.ylabel("My y label")
# plt.title("My title")

# plots.remove_frame()
style.despine()
# plt.grid()
# style.tighten()
# plt.tight_layout()
# plt.savefig("temp.pdf", transparent=True)

import colorsys
def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    red = int(round(red))
    green = int(round(green))
    blue = int(round(blue))
    return '#%02x%02x%02x' % (red, green, blue)

def hls_to_hex(hue, lightness, saturation):
    rgb_val = np.array(colorsys.hls_to_rgb(hue, lightness, saturation))*255
    return rgb_to_hex(*rgb_val)

plt.figure(2)
lightness = np.linspace(0.3, 0.70, 3)
markers = ['o', 's', 'v']
main = [103/360, 207/360, 311/360]
for j in range(3):
    for i in range(3):
        color = hls_to_hex(main[j], lightness[i], .55)
        plt.plot(x,(i+1)*x + 4*j*x**2, marker=markers[i], color = color, markevery=10, markersize=9)
plt.show()
