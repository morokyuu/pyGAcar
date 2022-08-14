# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def rot(th):
    return np.array([
        [np.cos(th), -np.sin(th), 0.0],
        [np.sin(th), np.cos(th), 0.0],
        [0.0, 0.0, 1.0],
        ])

def trans(dx,dy):
    return np.array([
        [1.0, 0.0, dx],
        [0.0, 1.0, dy],
        [0.0, 0.0, 1.0]
        ])

def mirrorX():
    return np.array([
        [-1,0,0],
        [0,1,0],
        [0,0,1]
        ])

def drawLine(ax, xy, color="green"):
    _,c = xy.shape
    xy = xy[0:2,:]
    for i in range(0,c,2):
        prt = xy[:,i:i+2]
        ax.plot(prt[0,:],prt[1,:], color=color)

def drawCircle(ax, xy, _r=2, _fc='b'):
    _,c = xy.shape
    xy = xy[0:2,:]
    for i in range(c):
        ax.add_patch(patches.Circle(xy[:,i], radius=_r, fc=_fc))

#robot size
BODY_W = 40
BODY_L = 70
THICK = 5
DIAMETER = 30

body = np.array([
    [0,0,1],
    [BODY_W, 0,1],
    [BODY_W, BODY_L,1],
    [0, BODY_L,1],
    ]).T

tire = np.array([
    [0,0,1],
    [THICK, 0,1],
    [THICK, DIAMETER,1],
    [0, DIAMETER,1],
    ]).T

sens = np.array([
    [BODY_W - 8, 65, 1]
    ]).T


ax = plt.subplot(1, 1, 1)

body = np.dot(trans(-BODY_W/2.0, -DIAMETER/2.0),body)
tireR = np.dot(trans(BODY_W/2.0, -DIAMETER/2.0),tire)
tireL = np.dot(mirrorX(),tireR)
sensR = np.dot(trans(-BODY_W/2.0, -15),sens)
sensL = np.dot(mirrorX(),sensR)

drawCircle(ax, body)
drawCircle(ax, tireR)
drawCircle(ax, tireL)
drawCircle(ax, sensR)
drawCircle(ax, sensL)

ax.set_xlabel("X [mm]")
ax.set_ylabel("Y [mm]")

plt.axis('scaled')
ax.set_aspect('equal')

PLOTAREA_WIDTH = 80.0
ax.set_xlim([-PLOTAREA_WIDTH, PLOTAREA_WIDTH])
ax.set_ylim([-PLOTAREA_WIDTH, PLOTAREA_WIDTH])
ax.grid()