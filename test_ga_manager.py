# -*- coding: utf-8 -*-
"""

"""

import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import ga_manager as gagm
import random
import sim_loop as sl

class GAManagerTest(unittest.TestCase):
    def setUp(self):
        print("setUp===")
        self.gm = gagm.GA_manager()

    def tearDown(self):
        pass

    def test_make_first_generation(self):
        self.gm.make_first_generation()
        #print(self.gm.genes)

        self.assertEqual(len(self.gm.genes),gagm.CAR_NUM)
        self.assertEqual(len(self.gm.genes[0]),sl.GEN_NUM)

    def test_choice_by_roulette(self):
        def score():
            return random.random()*100

        genes = []
        for i in range(gagm.CAR_NUM):
            g = list(int(b) for b in bin(2**(sl.ACTION_NUM//2)+i)[3:]) 
            genes += [(score(),g)]
        #print(genes)

        for gi in genes:
            print(f"{gi[0]:5.2f},{gi[1]}")
            #print(f"{gi[0]:.4g},{gi[1]:.4g}")
        
        

        self.gm.choice_by_roulette(genes,2)
        pass



if __name__ == "__main__":
    unittest.main()

