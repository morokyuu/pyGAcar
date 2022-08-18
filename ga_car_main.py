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
        self.dump = ""

    def exec(self):
        coursePix = np.array(Image.open('data/debug_course.jpg').convert('L')) 

        genes = []
        for i in range(gm.CAR_NUM):
            gene = self.gm.get_gene(i)
            #print(f"gene {i} = {gene[:20]}")
            sim = sl.SimLoop(cm.Pose(400,300,np.pi),coursePix,gene)
            score, self.dump = sim.exec()

            genes += [(score,gene)]
        #print(genes)

        ms = max(genes,key=lambda x: x[0])
        print(f"max score={ms[0]:.7g}")

        self.gm.make_next_generation(genes)
        return self.dump

def main():
    gac = GAcar_main()

    for _ in range(3):
        dump = gac.exec()
    print(dump)

if __name__ == "__main__":
    main()


