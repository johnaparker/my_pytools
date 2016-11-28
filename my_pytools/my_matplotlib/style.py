
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns


# plt.style.use('ggplot')
# sns.set(font_scale=8.8/11)
sns.set_style("white")
sns.set_context("paper", rc={"lines.linewidth": 1.5})
sns.set_style({'font.family': "Times New Roman", 'text.color': "black", 'axes.labelcolor': '0.0',
    'xtick.color': '0.0', 'ytick.color': '0.0'})
sns.set_palette("Paired")

flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
sns.set_palette(sns.color_palette(flatui))

colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
sns.set_palette(sns.xkcd_palette(colors))


colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628" , "#f781bf"]
sns.set_palette(sns.color_palette(colors))

unit_x = 0.8
unit_y = 0.8

# sns.set_context("talk", font_scale=2, rc={"lines.linewidth": 4})
# sns.set_style({'font.family': "Times New Roman"})
# unit_x = 5
# unit_y = 5
