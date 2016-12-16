import numpy as np
import matplotlib.pyplot as plt
import my_pytools.my_matplotlib.style as style
import my_pytools.my_matplotlib.plots as plots
import matplotlib

figsize = style.screen()

# main_colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628" , "#f781bf"]
# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628" , "#f781bf"]
# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628" , "#f781bf"]
# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#ffbf00", "#984ea3", "#a65628" , "#f781bf"]
# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#ffbf00", "#984ea3", "#802b00" , "#f781bf"]
# colors = ["#e41a1c", "#377eb8", "#4daf4a", "#ffbf00", "#9900cc", "#f781bf", "#00cccc", "#802b00"]
#          red        blue        green       orange   purple     pink       brown
#ff8000
# style.set_colors(colors)



import colorsys
def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    red = int(round(red))
    green = int(round(green))
    blue = int(round(blue))
    return '#%02x%02x%02x' % (red, green, blue)

def hls_to_hex(hue, lightness, saturation):
    rgb_val = np.array(colorsys.hls_to_rgb(hue, lightness, saturation))*255
    return rgb_to_hex(*rgb_val)

def hex_to_hls(hex_val):
    rgb_val = np.array(hex_to_rgb(hex_val))/255.0
    return np.array(colorsys.rgb_to_hls(*rgb_val))

def color_i(i, lightness=None):
    hls_val = hex_to_hls(main_colors[i])
    if lightness != None:
        hls_val[1] = lightness 
    new_hex = hls_to_hex(*hls_val)
    print(main_colors[i])
    print(new_hex)
    return new_hex

red = lambda lightness=None: color_i(0,lightness)
blue = lambda lightness=None: color_i(1,lightness)
green = lambda lightness=None: color_i(2,lightness)
purple = lambda lightness=None: color_i(3,lightness)
orange = lambda lightness=None: color_i(4,lightness)
brown = lambda lightness=None: color_i(5,lightness)
pink = lambda lightness=None: color_i(6,lightness)

# main_colors = [rgb_to_hex(57,106,177),
               # rgb_to_hex(218,124,48),
               # rgb_to_hex(62,150,81),
               # rgb_to_hex(204,37,41),
               # rgb_to_hex(83,81,84),
               # rgb_to_hex(107,76,154),
               # rgb_to_hex(146,36,40),
               # rgb_to_hex(148,139,61)]

main_colors = ["#066fba", "#d74c11","#ecaf1c", "#7b2b8b", "#72a92a", "#d40000", "#0000ff", "#6c5353"]

# style.set_colors(main_colors)

plt.figure(1, figsize=figsize.get())

x = np.linspace(-1,1,100)
for i in range(8):
    plt.plot(x,x+7-i, label= "plot {}".format(i), linewidth=4)

plt.legend(loc=2, frameon=True)
plt.xlabel("x label")
plt.ylabel("y label")


plt.figure(2, figsize=figsize.get())
import numpy.random as random
for i in range(8):
    scale = random.uniform(0.6,2.4)
    x = random.normal(size=100, loc=4*i, scale=scale)
    plt.hist(x, alpha=0.7, bins=10, label = "dist. {}".format(i))
plt.gca().legend(frameon=True, bbox_to_anchor=(1.2,1.05), shadow=True)
# plt.xlim(xmin=-20)

plt.xlabel("x label")
plt.ylabel("y label")

plt.figure(3)
plt.axis('off')
for i in range(8):
    rc = plt.Rectangle((i*15,0), 10, 10, fc=style.main_colors[i])
    plt.gca().add_patch(rc)
    rgb = hex_to_rgb(style.main_colors[i])
    plt.text(i*15, -4, "r: {0}".format(rgb[0]), fontsize=12)
    plt.text(i*15, -7, "g: {0}".format(rgb[1]), fontsize=12)
    plt.text(i*15, -10, "b: {0}".format(rgb[2]), fontsize=12)
    plt.text(i*15, 11, "color {0}".format(i), fontsize=12)
plt.xlim([-5, 120])

plt.axis('equal')
plt.show()

