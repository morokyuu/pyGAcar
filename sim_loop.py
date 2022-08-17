# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw
import car_model as cm

class SimLoop:
    def __init__(self,pose,course):
        self.pose = pose
        self.course = course
        self.car = cm.Car()

    def _sens2state(self,sens):
        return sens[0] * 2 + sens[1]


    def exec(self):
        # get sensor state 
        sens = self.car.get_sens(self.pose,self.course)
        state = self._sens2state(sens)

        print(state)

        # car control based on sensor state
        vl = 1
        vr = 2

        # car movement
        self.car.calc_steer(self.pose,vl,vr)


def main():
    coursePix = np.array(Image.open('data/debug_course.jpg').convert('L')) 
    sim = SimLoop(cm.Pose(400,300,np.pi),coursePix)
    for _ in range(70):
        sim.exec()

if __name__ == "__main__":
    main()
