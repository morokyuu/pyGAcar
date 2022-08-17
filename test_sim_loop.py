# -*- coding: utf-8 -*-
"""

"""

import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import car_model as cm
import sim_loop as sl
import random

class SimLoopTest(unittest.TestCase):
    def setUp(self):
        print("setUp===")
        coursePix = np.array(Image.open('data/debug_course.jpg').convert('L')) 

        #self.gene = list(random.choice([1,0]) for _ in range(sl.GEN_NUM))
        self.gene = [0] * sl.GEN_NUM

        self.sim = sl.SimLoop(cm.Pose(400,300,np.pi),coursePix,self.gene)

    def tearDown(self):
        pass

    def test_gene2index(self):
        gene = [0,1,1,0,0]
        idx = self.sim._gene2index(gene)
        self.assertEqual(12,idx)

    def _print_separate(self,a,length):
        spl = list(a[i:i+length] for i in range(0,len(a),length))
        for s in spl:
            print(s)

    def test_gene2part(self):
        state = [3,3,3]
        targ_gene = [1,1,1,0,0] + [1,0,0,0,1]

        stidx = sum([s * sl.STATE_PATTERN**n for n,s in enumerate(state[::-1])])
        idx = stidx*sl.ACTION_NUM
        print(f"state,stidx,idx={state},{stidx},{idx}")

        self.gene = self.gene[:idx] + targ_gene + self.gene[idx+sl.ACTION_NUM:]  
        self._print_separate(self.gene,sl.ACTION_NUM)

        print(idx)
        val = self.sim._gene2part(self.gene,state)

        self.assertEqual(idx,630)
        self.assertEqual(val,targ_gene)

#    def test_calc_wheel_speed(self):
#        print("calc_wheel_speed 1===")
#        state = [0,0,0,1]
#        vl,vr = self.sim._calc_wheel_speed(state,self.gene)
#        self.assertEqual(0,0)

#    def test_sens_(self):
#        self.pose = cm.Pose(400,300,np.pi)
#        sens = self.car.get_sens(self.pose,self.coursePix)
#        print(f"sens(L,R) = {sens}")
#        self.assertEqual((1,0),sens)

if __name__ == "__main__":
    unittest.main()

