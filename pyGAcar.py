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
STATE_PATTERN = 4
STATE_NUM=STATE_PATTERN**STATE_T_NUM
ACTION_NUM=5*2 #speed:5bit * 2motor
GEN_NUM=ACTION_NUM * STATE_NUM # length of single gene
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

def calc_car_position(x,y,th):
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

    def __init__(self,gene):
        self.sx = 500 
        self.sy = 330
        self.sq = 0
        self.state_t = []
        self.gene = gene
        self.score = 0

    

    def clamp(self,n,smallest,largest):
        return max(smallest,min(n,largest))

    def get_state(self,sensR,sensL,course):
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

    def get_sensor(self,course):
        self.body,self.sensR,self.sensL,self.tireR,self.tireL = calc_car_position(self.sx,self.sy,self.sq)
        state = self.get_state(self.sensR,self.sensL,course)

        self.state_t = self.state_t + [state]
        if len(self.state_t) > STATE_PATTERN-1:
            self.state_t = self.state_t[1:]
        print(self.state_t)

    def bin2int(self,gene_part):
        sep = int(ACTION_NUM/2)
        left  = int(''.join([str(g) for g in gene_part[:sep]]),2)
        right = int(''.join([str(g) for g in gene_part[sep:ACTION_NUM]]),2)
        return left,right

    def set_action(self):
        stidx = sum([s * STATE_PATTERN**n for n,s in enumerate(self.state_t[::-1])])

        idx = stidx*ACTION_NUM
        gene_part = self.gene[idx:idx+ACTION_NUM]
        print(f"idx={idx},gene_part={gene_part}")

        left,right = self.bin2int(gene_part)
        vel_L = speed_tbl[left]
        vel_R = speed_tbl[right]
        #print(f"gene_part={gene_part}, left,right={left},{right}")

        if self.state_t[-1] == 1 or self.state_t[-1] == 2:
            self.score += abs(vel_L + vel_R) / 2.0
        else:
            self.score += abs(vel_L + vel_R) / 2.0 * 0.2
        return vel_L, vel_R

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

    def run(self,course):
        self.get_sensor(course)
        vel_L,vel_R = self.set_action()

        self.move(vel_L,vel_R)

        pg.draw.polygon(screen,(100,100,100), self.body)
        pg.draw.polygon(screen,(80,100,100), self.tireR)
        pg.draw.polygon(screen,(80,100,100), self.tireL)
        sensCol = [(50,50,0),(200,200,0)]
        sensPat = [
            [sensCol[0],sensCol[0]],
            [sensCol[0],sensCol[1]],
            [sensCol[1],sensCol[0]],
            [sensCol[1],sensCol[1]],
        ]
        pg.draw.circle(screen, sensPat[self.state_t[-1]][0], self.sensL,4)
        pg.draw.circle(screen, sensPat[self.state_t[-1]][1], self.sensR,4)

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

        # generate genes
        self.ga = GA()
        self.ga.make_first_generation()

    
    def loop_sim(self,car):
        for t in range(SIM_COUNT):
            screen.fill((0,0,0))
            screen.blit(self.background,(0,0))

            info = mono_font.render("time"+str(t), True, (255,0,0))
            screen.blit(info, (20,20))

            car.run(self.coursePix)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        btn_space = True
                    elif event.key == pg.K_ESCAPE:
                        self.running = False

            pg.display.flip()
            fpsClock.tick(FPS)

    def execute(self):
        self.running = True
        self.car = list(Car(self.ga.get_gene(i)) for i in range(CAR_NUM))
#        for c in self.car:
#            self.loop_sim(c)
        self.loop_sim(self.car[0])
    



# =============================================================================
# start
# =============================================================================

speed_tbl = np.linspace(-1,1,32)


if False:
#if True:
    ga = GA()
    ga.make_first_generation()
    #print(ga.get_gene(0))

    state = [3,3,3]
    car = 0

    stidx = sum([s * STATE_PATTERN**n for n,s in enumerate(state[::-1])])
    gene = ga.get_gene(car)
    
    idx = stidx*ACTION_NUM
    gene_part = gene[idx:idx+ACTION_NUM]
    print(gene_part)

    left,right = bin2int(gene_part)
    print(f"{left},{right}")
    print(f"{speed_tbl[left]},{speed_tbl[right]}")

    
else:
    pg.init()

    screen = pg.display.set_mode([WINDOW_W, WINDOW_H])
    pg.display.set_caption("tameshi base")
    clock = pg.time.Clock()
    mono_font = pg.font.Font("/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf", 20)

    sim = Simulation(300,300)
    sim.execute()

    pg.quit()
