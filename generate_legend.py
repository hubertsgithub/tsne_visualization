import pylab
import numpy as np

CAT_TO_BORDER_COLOR = {
        "ceramic": np.array((250, 190, 190)),
        "fabric": np.array((145, 30, 180)),
        "foliage": np.array((60, 180, 75)),
        "glass": np.array((70, 240, 240)),
        "liquid": np.array((0, 130, 200)),
        "metal": np.array((128, 128, 128)),
        "paper": np.array((255, 250, 200)),
        "skin": np.array((255, 215, 180)),
        "stone": np.array((255, 225, 25)),
        "wood": np.array((170, 110, 40)),
}

c = []
keep_cats = []
for k,v in CAT_TO_BORDER_COLOR.items():
    c.append([float(c_ij) / 255 for c_ij in v])
    keep_cats.append(k)

fig = pylab.figure()
figlegend = pylab.figure(figsize=(3, 3))
ax = fig.add_subplot(111)

lines = []
plotted = []
for i,k in enumerate(keep_cats):
    lines.append(ax.scatter(0, 0, lw=0.5, s=300,
                            marker='o', edgecolor='k', color=c[i]))
    plotted.append(k)

figlegend.legend(lines, plotted, 'center', scatterpoints=1)
figlegend.savefig('legend.png')
