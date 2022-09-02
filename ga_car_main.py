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

import datetime
def get_timestamp():
    now = datetime.datetime.now()
    return "{0:%y%m%d%H%M%S}".format(now)

class GAcar_main:
    def __init__(self):
        self.generation = 0
        self.gm = gm.GA_manager()
        self.gm.make_first_generation()
        self.dump = ""

    def exec(self,dump_enb):
        self.generation += 1
        coursePix = np.array(Image.open('data/course2.jpg').convert('L')) 

        genes = []
        for i in range(gm.CAR_NUM):
            gene = self.gm.get_gene(i)
            #print("gene {0} = {1}".format(i,gene[:20]))

            sim = sl.SimLoop(cm.Pose(544,288,np.pi),coursePix,gene)
            if i == 0:
                score, self.dump = sim.exec()
            else:
                score, _ = sim.exec()

            genes += [(score,gene)]

        #ms = max(genes,key=lambda x: x[0])
        #print("max score={0:.7g}".format(ms[0]),flush=True)

        if dump_enb:
            self.do_dump(genes)

        self.gm.make_next_generation(genes)


    def do_dump(self,genes):
        stamp = get_timestamp()

        trail_name = "temp_dump/xyqs_"+stamp+".txt"
        with open(trail_name,"w") as fp:
            fp.write(self.dump)

        genes = sorted(genes,key=lambda x: x[0],reverse=True)
        print("max score={0:.7g}".format(genes[0][0]),flush=True)

        gene_name = "temp_dump/gene_"+stamp+".txt"
        with open(gene_name,"w") as fp:
            fp.write(f"generation={self.generation}"+"\n")
            fp.write(f"max score="+str(genes[0][0])+"\n") #score
            fp.write(str(genes[0][1])+"\n") #gene

def main():
    gac = GAcar_main()
    dump_enb = False
    LOOP_NUM = 1000

    for n in range(LOOP_NUM+1):
        if n % 50 == 0:
            dump_enb = True
        else:
            dump_enb = False
        gac.exec(dump_enb)

if __name__ == "__main__":
    main()


