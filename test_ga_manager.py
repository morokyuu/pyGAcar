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

        genes = sorted(genes, key=lambda x: x[0], reverse=True)
        for gi in genes:
            print(f"{gi[0]:5.2f},{gi[1]}")

        ga_1st = genes[0][1]
        ga_2nd = genes[1][1]
        print(f"{genes[0][1]}")
        print(f"{genes[1][1]}")

        count = 0
        for _ in range(100):
            choices = self.gm.choice_by_roulette(genes,2)
            #print(choices)
            if ga_1st == choices[0][1]:
                count += 1
            if ga_2nd == choices[1][1]:
                count += 1

        print(f"count={count}")
        pass



if __name__ == "__main__":
    unittest.main()

