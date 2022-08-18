# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw
import car_model as cm
import random
import ga_manager as gm
import sim_loop as sl

class GAcar_main:
    def __init__(self):
        self.gm = gm.GA_manager()
        self.gm.make_first_generation()

    def exec(self):
        coursePix = np.array(Image.open('data/debug_course.jpg').convert('L')) 
        #print(f"GEN_NUM={GEN_NUM}")

        genes = []
        for i in range(gm.CAR_NUM):
            gene = self.gm.get_gene(i)
            sim = sl.SimLoop(cm.Pose(400,300,np.pi),coursePix,gene)
            score = sim.exec()

            genes += [(score,gene)]
        print(genes)

def main():
    gac = GAcar_main()
    gac.exec()
    pass

if __name__ == "__main__":
    main()


