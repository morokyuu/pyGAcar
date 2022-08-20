# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image, ImageDraw

WINDOW_W = 600
WINDOW_H = 600

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
        self.BODY_L = 60
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

        #lidar-rays
        RAY_NUM = 6
        cent = 0+1.0j
        rpoint = 1/2.0 + np.sqrt(3)/2.0j #If RAY_NUM changed, rpoint should be changed too.
        #ray_length = 140.0
        ray_length = 100.0
        end_points = np.array(list(list([ray_length * np.real(p),ray_length * np.imag(p),1]) for p in (cent * (rpoint)**i for i in range(RAY_NUM))))
        #print(end_points)
        org_points = np.hstack((np.zeros((RAY_NUM,2)),np.ones((RAY_NUM,1))))
        self.ray = np.reshape(np.hstack((end_points,org_points)),(RAY_NUM*2,3)).T
        #print(self.ray)

        self.body = np.dot(trans(-self.BODY_W/2.0, -self.BODY_L/2.0),self.body)
        self.tireR = np.dot(trans(self.BODY_W/2.0, -self.DIAMETER/2.0),self.tire)
        self.tireL = np.dot(mirrorX(),self.tireR)
        self.ray = np.dot(trans(0, 20),self.ray)

    def _calc_cross_point(self,line0_xy,line1_xy):
        #a = np.array(line1_xy[0])-np.array(line0_xy[0])
        a = line1_xy[:,0]-line0_xy[:,0]
        b = line1_xy[:,1]-line0_xy[:,0]
        c = line0_xy[:,1]-line0_xy[:,0]
        #print(a,b,c)
        A = np.array([
            [a[0] - b[0], -c[0]],
            [a[1] - b[1], -c[1]]
            ])
        Bv = np.array([
            [-b[0]],
            [-b[1]]
            ])
        A_inv = np.linalg.inv(A)
        #print(A_inv)
        
        st = np.dot(A_inv, Bv)
        s_on = 0 < st[0] and st[0] < 1
        t_on = 0 < st[1] and st[1] < 1
        print(f"st:\n{st}\n s_on {s_on}, t_on {t_on}")
        flag = s_on and t_on

        #return flag, tuple(st[1] * c)
        cp = np.array([np.array(st[1] * c) + line0_xy[:,0]]).T

        return flag, cp


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

        cl = cr = 0
        return cl,cr


def main():
    car = Car()

    pose = Pose(400,300,np.pi)

    for i in range(1):  #(3.14/2)/0.025 = 68
        car.calc_steer(pose, 1,2)
        #print(f"q={pose.q:.4g}, x={pose.x:.4g}, y={pose.y:.4g}")
        #cl,cr = car.get_sens(pose,coursePix)

        #if False:
        if True:
            ax = plt.subplot(1, 1, 1)

            dv = pose.get_tf()
            print(dv)
            c_body  = dv @ car.body
            c_tireR = dv @ car.tireR
            c_tireL = dv @ car.tireL
            c_ray = dv @ car.ray
            drawCircle(ax, c_body , _fc='g')
            drawCircle(ax, c_tireR, _fc='g')
            drawCircle(ax, c_tireL, _fc='g')
            drawCircle(ax, c_ray, _fc='r', _r=2)
            
            #walls
            walls = np.array([[300,0,1],[600,300,1],[300,600,1],[0,300,1]])
            walls = np.reshape(np.hstack((walls, np.roll(walls,3*3))),(8,3)).T
            drawLine(ax,walls)

#            #ray0 = c_ray[:,10:13]
#            ray0 = c_ray[:,2:4]
#            drawLine(ax, ray0, color="yellow")
#            hit,crosspoint = car._calc_cross_point(ray0,l1)
#            drawCircle(ax, crosspoint, _r=3)


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
