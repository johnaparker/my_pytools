import numpy as np
import matplotlib.pyplot as plt
import my_pytools.my_matplotlib.style as style
import my_pytools.my_matplotlib.colors as colors
import my_pytools.my_matplotlib.plots as plots
import matplotlib

from matplotlib.backends.backend_pdf import PdfPages

figsize = style.screen()


other_palettes = [
            ["#ff0000", "#0066ff", "#89a02c", "#800080", "#ff7f2a", "#a05a2c", "#ff55dd", "#4d4d4d"],
            ["#066fba", "#d74c11","#ecaf1c", "#7b2b8b", "#72a92a", "#d40000", "#0000ff", "#6c5353"],

            [colors.rgb_to_hex(57,106,177),
               colors.rgb_to_hex(218,124,48),
               colors.rgb_to_hex(62,150,81),
               colors.rgb_to_hex(204,37,41),
               colors.rgb_to_hex(83,81,84),
               colors.rgb_to_hex(107,76,154),
               colors.rgb_to_hex(146,36,40),
               colors.rgb_to_hex(148,139,61)],

            [colors.rgb_to_hex(0,0,0),
               colors.rgb_to_hex(230,159,0),
               colors.rgb_to_hex(86,180,233),
               colors.rgb_to_hex(0,158,115),
               colors.rgb_to_hex(240,228,66),
               colors.rgb_to_hex(0,114,178),
               colors.rgb_to_hex(213,94,0),
               colors.rgb_to_hex(204,121,167)],
            ["#ff0000", "#0000ff", "#89a02c", "#800080", "#ff7f2a", "#a05a2c", "#ff55dd", "#000000"],
            ]

palettes = colors.color_palettes.values()

import numpy.random as random
with PdfPages("test.pdf") as pdf:
    for pal_num,palette_name in enumerate(colors.color_palettes.keys()):
        palette = colors.color_palettes[palette_name]
        colors.set_colors_list(palette)
        # fig = plt.figure(1, figsize=(18,12))
        fig = plt.figure(pal_num+1, figsize=(18,12))
        ax = plt.subplot2grid((3,6), (1,0), rowspan=2, colspan=3)

        x = np.linspace(-1,1,100)
        for i in range(8):
            noise = random.random(100)*.7
            plt.plot(x,x+7-i+noise, label= "plot {}".format(i+1), linewidth=4)

        plt.tight_layout()
        plt.ylim([-1,11])
        plt.legend(loc=2, ncol=3,frameon=True, shadow=True)
        plt.xlabel("x label")
        plt.ylabel("y label")



        ax = plt.subplot2grid((3,6), (1,3), rowspan=2, colspan=3)
        for i in range(8):
            scale = random.uniform(0.6,2.4)
            scale=1.4
            x = random.normal(size=100, loc=4*i, scale=scale)
            plt.hist(x, alpha=0.7, bins=10, label = "dist. {}".format(i+1))
        # plt.gca().legend(frameon=True, bbox_to_anchor=(1.2,1.05), shadow=True)
        plt.gca().legend(loc=2,frameon=True, ncol=3, shadow=True)
        # plt.xlim(xmin=-20)

        plt.xlabel("x label")
        plt.ylabel("y label")
        plt.ylim([0,32])

        plt.tight_layout()
        # plt.figure(3)
        ax = plt.subplot2grid((3,6), (0,0), rowspan=1, colspan=6)
        plt.axis('off')
        for i in range(8):
            rc = plt.Rectangle((i*15,0), 10, 10, fc=palette[i])
            plt.gca().add_patch(rc)
            rgb = colors.hex_to_rgb(palette[i])
            plt.text(i*15, -2.5, "r: {0}".format(rgb[0]))
            plt.text(i*15, -5, "g: {0}".format(rgb[1]))
            plt.text(i*15, -7.5, "b: {0}".format(rgb[2]))
            plt.text(i*15, 11, "color {0}".format(i+1))
        plt.xlim([-5, 120])
        plt.text(60, 15, palette_name, horizontalalignment='center', fontsize=30, weight='semibold')
        plt.axis('equal')
        # plt.savefig("temp.pdf", transparent=True)
        pdf.savefig()

# plt.show()

