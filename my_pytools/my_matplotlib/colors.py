import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
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

def hex_to_hls(hex_val):
    rgb_val = np.array(hex_to_rgb(hex_val))/255.0
    return np.array(colorsys.rgb_to_hls(*rgb_val))

def colors(i, lightness=None):
    """get color index i with desired lightness"""
    hls_val = hex_to_hls(current_palette[i])
    if lightness != None:
        hls_val[1] = lightness 
    new_hex = hls_to_hex(*hls_val)
    return new_hex

#          red        blue        green       purple   orange     brown        pink      gray       

blue = lambda lightness=None: colors(0,lightness)
orange = lambda lightness=None: colors(1,lightness)
green = lambda lightness=None: colors(2,lightness)
red = lambda lightness=None: colors(3,lightness)
purple = lambda lightness=None: colors(4,lightness)
brown = lambda lightness=None: colors(5,lightness)
pink = lambda lightness=None: colors(6,lightness)
gray = lambda lightness=None: colors(7,lightness)

def set_colors_list(colors):
    """set current color cycle to colors (list)"""
    global current_palette
    current_palette = colors
    mpl.rcParams.update({'axes.prop_cycle': mpl.cycler('color', colors)})

def set_colors(palette):
    """set current color cycle to existing pallete"""
    set_colors_list(color_palettes[palette])


color_palettes = {
    "main" : ["#0066ff", rgb_to_hex(255,127,14), "#89a02c", "#ff0000", "#7b2b8b", "#a05a2c", "#ff55dd", "#4d4d4d"],

    "main soft" : ["#377eb8", "#ff7f00", "#4daf4a", "#e41a1c", "#984ea3", "#a65628" , "#f781bf", "#666666"],

    "norbert" : ["#0000ff", "#ff7f2a", "#89a02c", "#ff0000", "#800080", "#a05a2c", "#ff55dd", "#222222"],

    "mpl2": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"],

    "palette1" : ["#066fba", "#d74c11","#ecaf1c", "#7b2b8b", "#72a92a", "#d40000", "#0000ff", "#6c5353"],

    "color blind" : [rgb_to_hex(0,0,0),
               rgb_to_hex(230,159,0),
               rgb_to_hex(86,180,233),
               rgb_to_hex(0,158,115),
               rgb_to_hex(240,228,66),
               rgb_to_hex(0,114,178),
               rgb_to_hex(213,94,0),
               rgb_to_hex(204,121,167)],
    }

default_palette = color_palettes['main']
current_palette = default_palette
set_colors_list(default_palette)


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    """return a truncated colormap from an existing one
            cmap        color map
            minval      lower bound
            maxval      upper bound
            n           number of values """
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


