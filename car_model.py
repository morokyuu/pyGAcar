# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image, ImageDraw

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


class Pose:
    def __init__(self,x,y,q):
        self.x = x
        self.y = y
        self.q = q

    def get_tf(self):
        return trans(self.x,self.y) @ rot(self.q)


class Car:
    def __init__(self):
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
            [-self.BODY_W/2.0 + 8, 65, 1]
            ]).T

        self.body = np.dot(trans(-self.BODY_W/2.0, -self.DIAMETER/2.0),self.body)
        self.tireR = np.dot(trans(self.BODY_W/2.0, -self.DIAMETER/2.0),self.tire)
        self.tireL = np.dot(mirrorX(),self.tireR)
        self.sensR = np.dot(trans(0, -15),self.sens)
        self.sensL = np.dot(mirrorX(),self.sensR)

    def calc_steer(self,pose,vel_L,vel_R):
        t_sq = (vel_L - vel_R) / self.BODY_W
        t_vel = (vel_L + vel_R) / 2.0
        #R = self.BODY_W/2.0 * (vel_R - vel_L) / (vel_R - vel_L+0.001)
        #print(f"t_sq={t_sq:.2g}, t_vel={t_vel:.2g}, R={R:.2g}")
        
        pose.x -= t_vel * np.sin(pose.q)
        pose.y += t_vel * np.cos(pose.q)
        pose.q += t_sq

        if pose.x < 0:
            pose.x += WINDOW_W
        if pose.x >= WINDOW_W:
            pose.x -= WINDOW_W
        if pose.y < 0:
            pose.y += WINDOW_H
        if pose.y >= WINDOW_H:
            pose.y -= WINDOW_H
        #print(f"pose.q={pose.q:.2g}, pose.x={pose.x:.2g}, pose.y={pose.y:.2g}")

    def threshold(self,sens_value):
        if sens_value < 128:
            return 0
        else:
            return 1

    def get_sens(self,pose,pix):
        def clamp(val,maxval):
            return int(max(min(maxval,val),0))

        sr = pose.get_tf() @ self.sensR
        sl = pose.get_tf() @ self.sensL

        srx,sry,_ = list(int(v) for v in sr)
        slx,sly,_ = list(int(v) for v in sl)

        cr = pix[clamp(sry,WINDOW_H-1),clamp(srx,WINDOW_W-1)]
        cl = pix[clamp(sly,WINDOW_H-1),clamp(slx,WINDOW_W-1)]
        #print(f"sensL: pix[{slx},{sly}]={cl} sensR: pix[{srx},{sry}]={cr}")

        cr = self.threshold(cr)
        cl = self.threshold(cl)
        return cl,cr


def main():

    coursePix = np.array(Image.open('data/debug_course.jpg').convert('L')) 
    
    car = Car()

    pose = Pose(400,300,np.pi)

    for i in range(67):  #(3.14/2)/0.025 = 68
    #for i in range(1):  #(3.14/2)/0.025 = 68
        car.calc_steer(pose, 1,2)
        #print(f"q={pose.q:.4g}, x={pose.x:.4g}, y={pose.y:.4g}")
        cl,cr = car.get_sens(pose,coursePix)

        #if False:
        if True:
            ax = plt.subplot(1, 1, 1)

            dv = pose.get_tf()
            print(dv)
            c_body  = dv @ car.body
            c_tireR = dv @ car.tireR
            c_tireL = dv @ car.tireL
            c_sensR = dv @ car.sensR
            c_sensL = dv @ car.sensL
            drawCircle(ax, c_body , _fc='g')
            drawCircle(ax, c_tireR, _fc='g')
            drawCircle(ax, c_tireL, _fc='g')
            drawCircle(ax, c_sensR, _fc='r', _r=2)
            drawCircle(ax, c_sensL, _fc='r', _r=2)

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
                name = "car{0}.png".format(i)
                plt.savefig(name)
                plt.clf()

if __name__ == "__main__":
    main()
