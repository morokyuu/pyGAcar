#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
WINDOW_W = 640
WINDOW_H = 480

# df = pd.read_csv("../temp_xyq",header=None)
df = pd.read_csv("../temp_xyqs",header=None)
#print(df)

l = 80 
df[3] = l*np.sin(df[2])
df[4] = l*np.cos(df[2])
print(df)

fig, ax = plt.subplots()
ax.quiver(df[0],df[1],df[3],df[4], color='red', angles='xy', scale_units='xy', scale=1)
ax.scatter(df[0],df[1],s=1)
ax.set_xlabel("X [mm]")
ax.set_ylabel("Y [mm]")
ax.set_aspect('equal')
ax.set_xlim([0,WINDOW_W])
ax.set_ylim([0,WINDOW_H])
ax.invert_yaxis()
ax.grid()

plt.show()
