# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw
import car_model as cm

STATE_PTTERN = 4

class SimLoop:
    def __init__(self,pose,course):
        self.pose = pose
        self.course = course
        self.car = cm.Car()
        self.score = 0
        self.state = []

    def _sens2state(self,sens):
        return sens[0] * 2 + sens[1]

    def _calc_score(self, state, vel_L, vel_R):
        if state[-1] == 1 or state[-1] == 2:
            self.score += abs(vel_L + vel_R) / 2.0
        else:
            self.score += abs(vel_L + vel_R) / 2.0 * 0.2

    def exec(self):
        # get sensor state 
        sens = self.car.get_sens(self.pose,self.course)
        self.state = self.state + [self._sens2state(sens)]

        if len(self.state) > STATE_PTTERN-1:
            self.state = self.state[1:]
        print(self.state)

        # car control based on sensor state
        vl = 1
        vr = 2

        # calc GA score
        self._calc_score(self.state,vl,vr)
        print(self.score)

        # car movement
        self.car.calc_steer(self.pose,vl,vr)


def main():
    coursePix = np.array(Image.open('data/debug_course.jpg').convert('L')) 
    sim = SimLoop(cm.Pose(400,300,np.pi),coursePix)
    for _ in range(70):
        sim.exec()

if __name__ == "__main__":
    main()
