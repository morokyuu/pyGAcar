# -*- coding: utf-8 -*-
"""

"""

import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import sim_loop as sl

class SimLoopTest(unittest.TestCase):
    def setUp(self):
        coursePix = np.array(Image.open('data/debug_course.jpg').convert('L')) 
        self.sim = SimLoop(cm.Pose(400,300,np.pi),coursePix)
        pass

    def tearDown(self):
        pass

    def test_gene2index(self):
        gene = [0,1,1,0,0]
        idx = self.sim._gene2index(gene)
        self.assertEqual(12,idx)

    def test_calc_wheel_speed(self):
        state = [0,0,0,1]

    def test_sens_(self):
        self.pose = cm.Pose(400,300,np.pi)
        sens = self.car.get_sens(self.pose,self.coursePix)
        print(f"sens(L,R) = {sens}")
        self.assertEqual((1,0),sens)

if __name__ == "__main__":
    unittest.main()

