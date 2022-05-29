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

# window size
WINDOW_W = 640
WINDOW_H = 480

SCREENRECT = pg.Rect(0,0,640,480)
main_dir = os.path.split(os.path.abspath(__file__))[0]

# frame rate
FPS = 60
fpsClock = pg.time.Clock()

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
        
    def update(self,vel_L,vel_R):
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


        
    def draw(self):
        body,sensR,sensL,tireR,tireL = drawCar(self.sx,self.sy,self.sq)
        pg.draw.polygon(screen,(100,100,100), body)
        pg.draw.polygon(screen,(80,100,100), tireR)
        pg.draw.polygon(screen,(80,100,100), tireL)
        pg.draw.circle(screen,(200,200,0), sensR,4)
        pg.draw.circle(screen,(200,200,0), sensL,4)
        


class Simulation:
    def __init__(self):
        self.car = Car(300,300)
        self.background = load_image('course1.jpg')
        #self.background = pg.Surface(SCREENRECT.size)
    
    def mainloop(self,running):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    btn_space = True
                elif event.key == pg.K_ESCAPE:
                    running = False
        
        screen.fill((0,0,0))
        screen.blit(self.background, (0,0))
        pg.draw.rect(screen, (220,220,0), (0,0,32,32))
        
        self.car.update(0.55,0.6)
        self.car.draw()
        
        return running
    



# =============================================================================
# start
# =============================================================================

pg.init()

screen = pg.display.set_mode([WINDOW_W, WINDOW_H])
pg.display.set_caption("tameshi base")
clock = pg.time.Clock()
mono_font = pg.font.Font("/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf", 20)

sim = Simulation()
running = True

while running:
    running = sim.mainloop(running)
    
    pg.display.flip()
    fpsClock.tick(FPS)

pg.quit()
