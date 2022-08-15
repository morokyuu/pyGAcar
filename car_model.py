# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

WINDOW_W = 640
WINDOW_H = 480

def rot(th):
    return np.array([
        [np.cos(th), -np.sin(th), 0.0],
        [np.sin(th),  np.cos(th), 0.0],
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

def drawCircle(ax, xy, _r=1.4, _fc='b'):
    _,c = xy.shape
    xy = xy[0:2,:]
    for i in range(c):
        ax.add_patch(patches.Circle(xy[:,i], radius=_r, fc=_fc))


class Car:
    def __init__(self,ini_x=WINDOW_W/2.0,ini_y=WINDOW_H/2.0,ini_q=0.0):
        #robot size
        self.BODY_W = 40
        self.BODY_L = 70
        self.THICK = 5
        self.DIAMETER = 30

        self.body = np.array([
            [0,0,1],
            [self.BODY_W, 0,1],
            [self.BODY_W, self.BODY_L,1],
            [0, self.BODY_L,1],
            ]).T

        self.tire = np.array([
            [0,0,1],
            [self.THICK, 0,1],
            [self.THICK, self.DIAMETER,1],
            [0, self.DIAMETER,1],
            ]).T

        self.sens = np.array([
            [self.BODY_W - 8, 65, 1]
            ]).T

        self.sx = ini_x
        self.sy = ini_y
        self.sq = ini_q 

        self.body = np.dot(trans(-self.BODY_W/2.0, -self.DIAMETER/2.0),self.body)
        self.tireR = np.dot(trans(self.BODY_W/2.0, -self.DIAMETER/2.0),self.tire)
        self.tireL = np.dot(mirrorX(),self.tireR)
        self.sensR = np.dot(trans(-self.BODY_W/2.0, -15),self.sens)
        self.sensL = np.dot(mirrorX(),self.sensR)

    def calc_steer(self,vel_L,vel_R):
        t_sq = (vel_L - vel_R) / self.BODY_W
        t_vel = (vel_L + vel_R) / 2.0

        #R = self.BODY_W/2.0 * (vel_R - vel_L) / (vel_R - vel_L+0.001)
        #print(f"t_sq={t_sq:.2g}, t_vel={t_vel:.2g}, R={R:.2g}")
        
        self.sq += t_sq
        self.sx -= t_vel * np.sin(self.sq)
        self.sy += t_vel * np.cos(self.sq)

        if self.sx < 0:
            self.sx += WINDOW_W
        if self.sx >= WINDOW_W:
            self.sx -= WINDOW_W
        if self.sy < 0:
            self.sy += WINDOW_H
        if self.sy >= WINDOW_H:
            self.sy -= WINDOW_H
        #print(f"sq={self.sq:.2g}, sx={self.sx:.2g}, sy={self.sy:.2g}")



def main():
    car = Car(400,300,np.pi)

    for i in range(67):  #(3.14/2)/0.025 = 68
    #for i in range(1):  #(3.14/2)/0.025 = 68
        car.calc_steer(1,2)

        print(f"q={car.sq:.4g}, x={car.sx:.4g}, y={car.sy:.4g}")


        #if False:
        if True:
            ax = plt.subplot(1, 1, 1)
            dv = trans(car.sx,car.sy) @ rot(car.sq)
            print(dv)
            c_body  = dv @ car.body
            c_tireR = dv @ car.tireR
            c_tireL = dv @ car.tireL
            c_sensR = dv @ car.sensR
            c_sensL = dv @ car.sensL
            drawCircle(ax, c_body , _fc='g')
            drawCircle(ax, c_tireR, _fc='g')
            drawCircle(ax, c_tireL, _fc='g')
            drawCircle(ax, c_sensR, _fc='g')
            drawCircle(ax, c_sensL, _fc='g')

            ax.set_xlabel("X [mm]")
            ax.set_ylabel("Y [mm]")
            plt.axis('scaled')
            ax.set_aspect('equal')
            ax.set_xlim([0,WINDOW_W])
            ax.set_ylim([0,WINDOW_H])
            ax.invert_yaxis()
            ax.grid()
            plt.show()

            #if True:
            if False:
                name = f"car{i}.png"
                plt.savefig(name)
                plt.clf()

if __name__ == "__main__":
    main()
