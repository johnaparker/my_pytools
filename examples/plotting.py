import numpy as np
import matplotlib.pyplot as plt
import my_pytools.my_matplotlib.style as style
import my_pytools.my_matplotlib.plots as plots
import matplotlib

plt.figure(1, figsize=(3,2))
style.paper()

x = np.linspace(0,1,100)
y1 = x**1
y2 = x**2
y3 = x**3

plt.plot(x,y1, label= "plot 1")
plt.plot(x,y2, label= "plot 2")
plt.plot(x,y3, label= "plot 3")

plt.legend(loc='best')
plt.xlabel("My x label")
plt.ylabel("My y label")
# plt.title("My title")

# plots.remove_frame()
style.despine()
# plt.grid()
# style.tighten()
# plt.tight_layout()
plt.savefig("temp.pdf", transparent=True)
plt.show()
