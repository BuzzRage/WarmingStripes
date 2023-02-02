#!/usr/bin/env python3

# First draft based on https://matplotlib.org/matplotblog/posts/warming-stripes/

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
import pandas as pd
import sys

fr_data = False
filename = ""

args = list(sys.argv)
for arg in sys.argv:
    if arg in ["fr", "global"]:
        args.remove(arg)
        if arg == "fr":
            fr_data = True
        else:
            fr_data = False

FROM_t = 1850
TO_t   = 2018

# Reference period for the center of the color scale
FIRST_REFERENCE = 1971
LAST_REFERENCE = 2000
LIM = 0.7 # degrees

# data source:
# Global: https://www.metoffice.gov.uk/hadobs/hadcrut4/data/current/time_series/HadCRUT.4.6.0.0.annual_ns_avg.txt
# France: https://berkeleyearth.org/wp-content/themes/client-theme/temperature-data/France-projection.txt

if fr_data is True:
    filename = "data/france-projection-clean.txt"
else:
    filename = "data/HadCRUT.4.6.0.0.annual_ns_avg.txt"

data = pd.read_fwf(filename, index_col=0, cusecols=(0, 1), names=['year', 'anomaly'], header=None)

anomaly = data.loc[FROM_t:TO_t, 'anomaly'].dropna()
reference = anomaly.loc[FIRST_REFERENCE:LAST_REFERENCE].mean()

# the colors in this colormap come from http://colorbrewer2.org
# the 8 more saturated colors from the 9 blues / 9 reds
cmap = ListedColormap([
    '#08306b', '#08519c', '#2171b5', '#4292c6',
    '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
    '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a',
    '#ef3b2c', '#cb181d', '#a50f15', '#67000d',
])

fig = plt.figure(figsize=(10, 1))

ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()

# create a collection with a rectangle for each year
col = PatchCollection([
    Rectangle((y, 0), 1, 1)
    for y in range(FROM_t, TO_t + 1)
])

# set data, colormap and color limits

col.set_array(anomaly)
col.set_cmap(cmap)
col.set_clim(reference - LIM, reference + LIM)
ax.add_collection(col)

ax.set_ylim(0, 1)
ax.set_xlim(FROM_t, TO_t + 1)

if fr_data is True:
    fig.savefig('img/warming-stripes-fr.png')
else:
    fig.savefig('img/warming-stripes-global.png')
    
