#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 09:19:09 2022

@author: zotac
"""


import pygame as pg
import random
import numpy as np
import os
from PIL import Image
from enum import Enum


# window size
WINDOW_W = 640
WINDOW_H = 480

SCREENRECT = pg.Rect(0,0,640,480)
main_dir = os.path.split(os.path.abspath(__file__))[0]

# frame rate
FPS = 240
fpsClock = pg.time.Clock()

# define
BLACK = 0
WHITE = 1

# define 
SIM_COUNT=1000
STATE_T_NUM=3 # num of previous data
STATE_NUM=4**STATE_T_NUM
ACTION_NUM=5*2 #speed:5bit * 2motor
GEN_NUM=ACTION_NUM*STATE_NUM # length of single gene
CAR_NUM=10 # number of trial

# polygon usage
# https://programtalk.com/python-examples/pygame.draw.polygon/

def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()



def rot(th):
    return np.array([[np.cos(th), np.sin(th), 0],[-np.sin(th),np.cos(th), 0],[0,0,1]])

def tr(x,y):
    return np.array([[1,0,x],[0,1,y],[0,0,1]])

def mirrorX():
    return np.array([[-1,0,0],[0,1,0],[0,0,1]])


#robot size
BODY_W = 40
THICK = 5
RADIOUS = 15

def conv2vertlist(array):
    return list(list(array[:2,i]) for i in range(array.shape[1]))

def drawCar(x,y,th):
    body = np.array([
        [-BODY_W/2, -50, 1],
        [-BODY_W/2,  20, 1],
        [ BODY_W/2,  20, 1],
        [ BODY_W/2, -50, 1],
        ]).T
    A = tr(x,y) @ rot(th)
    body = np.dot(A, body)

    TIRE = np.array([
        [-THICK,-RADIOUS, 1],
        [-THICK, RADIOUS, 1],
        [ THICK, RADIOUS, 1],
        [ THICK,-RADIOUS, 1],
        ]).T
    TIRE_CENT = tr(BODY_W/2+5,0)
    TR = tr(x,y) @ rot(th) @ TIRE_CENT
    tireR = np.dot(TR, TIRE)
    TL = tr(x,y) @ rot(th) @ mirrorX() @ TIRE_CENT
    tireL = np.dot(TL, TIRE)

    SENS_CENT = tr(BODY_W/2-5,-50)
    sensR = (tr(x,y) @ rot(th) @ SENS_CENT)[:,2]
    sensL = (tr(x,y) @ rot(th) @ mirrorX() @ SENS_CENT)[:,2]
    
    body = conv2vertlist(body)
    tireR = conv2vertlist(tireR)
    tireL = conv2vertlist(tireL)
    sensR = list(sensR[:2])
    sensL = list(sensL[:2])
    
    return body,sensR,sensL,tireR,tireL


class Car:

    def __init__(self,init_x,init_y):
        self.sx = init_x
        self.sy = init_y
        self.sq = 0
        self.state_t = []

    def move(self,vel_L,vel_R):
        vel_L *= -1
        vel_R *= -1
        t_sq = (vel_L - vel_R) / BODY_W
        t_vel = (vel_L + vel_R) / 2.0
        
        self.sq += t_sq
        self.sx += t_vel * np.sin(self.sq)
        self.sy += t_vel * np.cos(self.sq)

        if self.sx < 0:
            self.sx += WINDOW_W
        if self.sx >= WINDOW_W:
            self.sx -= WINDOW_W
        if self.sy < 0:
            self.sy += WINDOW_H
        if self.sy >= WINDOW_H:
            self.sy -= WINDOW_H
    

    def clamp(self,n,smallest,largest):
        return max(smallest,min(n,largest))
    
    def sense(self,sensR,sensL,course):
        # position of sensorL,R
        sensR_idx = [
            int(self.clamp(sensR[0], 0, WINDOW_W-1)),
            int(self.clamp(sensR[1], 0, WINDOW_H-1))
        ]
        sensL_idx = [
            int(self.clamp(sensL[0], 0, WINDOW_W-1)),
            int(self.clamp(sensL[1], 0, WINDOW_H-1))
        ]

        # reading pixel value
        resL = resR = BLACK
        if course[sensR_idx[1],sensR_idx[0]] > 200:
            resR = WHITE
        if course[sensL_idx[1],sensL_idx[0]] > 200:
            resL = WHITE
        return resL,resR

    def get_state(self,resL,resR):
        state = 0
        if resL == BLACK and resR == BLACK:
            state = 0
        elif resL == BLACK and resR == WHITE:
            state = 1 
        elif resL == WHITE and resR == BLACK:
            state = 2 
        elif resL == WHITE and resR == WHITE:
            state = 3
        return state

    def update(self,vel_L,vel_R,course):
        self.move(vel_L, vel_R)
        
        body,sensR,sensL,tireR,tireL = drawCar(self.sx,self.sy,self.sq)
        resL,resR = self.sense(sensR,sensL,course)
        state = self.get_state(resL,resR)

        self.state_t = self.state_t + [state]
        if len(self.state_t) > STATE_T_NUM+1:
            self.state_t = self.state_t[1:]
        print(self.state_t)

        pg.draw.polygon(screen,(100,100,100), body)
        pg.draw.polygon(screen,(80,100,100), tireR)
        pg.draw.polygon(screen,(80,100,100), tireL)
        sensCol = [(50,50,0),(200,200,0)]
        pg.draw.circle(screen, sensCol[resL], sensL,4)
        pg.draw.circle(screen, sensCol[resR], sensR,4)

        #print(f"{self.resL}, {self.resR}, {state}")


class GA:
    def __init__(self):
        self.genes = []
        self.make_first_generation()
        pass

    def make_first_generation(self):
        for _ in range(CAR_NUM):
            self.genes.append([random.choice([1,0]) for _ in range(GEN_NUM)])
    
    def get_gene(self, i):
        return self.genes[i]





class Simulation:
    def __init__(self,intx,inty):
        # for display
        self.background = load_image('course1.jpg')
        # as a ndarray for sensing
        self.coursePix = np.array(Image.open('data/course1.jpg').convert('L'))
        # init car
        self.car = Car(intx,inty)

        self.running = True

    

    
    def mainloop(self):
    
        screen.fill((0,0,0))
        screen.blit(self.background, (0,0))
        pg.draw.rect(screen, (220,220,0), (0,0,32,32))
        self.car.update(0.55,0.6,self.coursePix)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    btn_space = True
                elif event.key == pg.K_ESCAPE:
                    self.running = False
        return self.running
    



# =============================================================================
# start
# =============================================================================

#ga = GA()
#ga.make_first_generation()
#print(ga.get_gene(0))

pg.init()

screen = pg.display.set_mode([WINDOW_W, WINDOW_H])
pg.display.set_caption("tameshi base")
clock = pg.time.Clock()
mono_font = pg.font.Font("/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf", 20)

sim = Simulation(300,300)
running = True

while running:
    running = sim.mainloop()
    
    pg.display.flip()
    fpsClock.tick(FPS)

pg.quit()
