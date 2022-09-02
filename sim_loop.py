# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw
import car_model as cm
import random

LOOP_NUM = 500
STATE_T_NUM=3 # num of previous data
STATE_PATTERN = 4
STATE_NUM=STATE_PATTERN**STATE_T_NUM
ACTION_NUM=5*2 #speed:5bit * 2motor
GEN_NUM=ACTION_NUM * STATE_NUM # length of single gene

class SimLoop:
    def __init__(self,pose,course,gene):
        self.pose = pose
        self.course = course
        self.car = cm.Car()
        self.state = []
        self.gene = gene
        self.speed_tbl = np.linspace(-5,5,2**5)

    def _sens2state(self,sens):
        return sens[0] * 2 + sens[1]

    def _calc_score(self, state, vel_L, vel_R):
        score = 0.0
        if state[-1] == 1 or state[-1] == 2:
            score = abs(vel_L + vel_R) / 2.0
        else:
            score = abs(vel_L + vel_R) / 2.0 * 0.2
        return score


    def _gene_to_speed_index(self,gene_part):
        return sum([s * 2**n for n,s in enumerate(gene_part[::-1])])

    def _state_to_gene_index(self,state):
        stidx = sum([s * STATE_PATTERN**n for n,s in enumerate(state[::-1])])
        idx = stidx*ACTION_NUM
        return idx

    def _calc_wheel_speed(self,state,gene):
        idx = self._state_to_gene_index(state)
        gene_part = gene[idx:idx+ACTION_NUM]

        sep = ACTION_NUM//2
        left  = self._gene_to_speed_index(gene_part[:sep])
        right = self._gene_to_speed_index(gene_part[sep:ACTION_NUM])

        vel_L = self.speed_tbl[left]
        vel_R = self.speed_tbl[right]
        return vel_L, vel_R

    def exec(self):
        dump = ""
        score = 0

        for _ in range(LOOP_NUM):
            # get sensor state 
            sens = self.car.get_sens(self.pose,self.course)
            self.state = self.state + [self._sens2state(sens)]

            if len(self.state) > STATE_T_NUM:
                self.state = self.state[1:]
            #print(self.state)

            # car control based on sensor state
            vl,vr = self._calc_wheel_speed(self.state,self.gene)

            # calc GA score
            score += self._calc_score(self.state,vl,vr)
            #print(self.score)

            # car movement
            self.car.calc_steer(self.pose,vl,vr)
            #print(f"{self.pose.x:.5g},{self.pose.y:.5g},{self.pose.q:.5g}")
            dump += "{0:10.3f},{1:10.3f},{2:10.5f},{3:3d}\n".format(self.pose.x,self.pose.y,self.pose.q,self.state[-1])
        return score,dump


def main():
    coursePix = np.array(Image.open('data/debug_course.jpg').convert('L')) 
    #print(f"GEN_NUM={GEN_NUM}")
    gene = list(random.choice([1,0]) for _ in range(GEN_NUM))
    sim = SimLoop(cm.Pose(400,300,np.pi),coursePix,gene)
    score,dump = sim.exec()
    print(score)

if __name__ == "__main__":
    main()
