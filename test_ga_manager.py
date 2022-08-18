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

    def test_mix_exception(self):
        with self.assertRaises(Exception):
            self.gm.mix([0,0,0])

    def test_mix_1(self):
#        #gene = list(list(random.choice([1,0]) for i in range(8)) for _ in range(4))
#        pair_num = 2
#        gene = ( [[1,0]*2] + [[0,1]*2] ) * pair_num
#
#        for i in range(0,2*pair_num,2):
#            print(f"before {gene[i]}, {gene[i+1]}")
#        
#        mixed_gene = self.gm.mix(gene)
#
#        for i in range(0,2*pair_num,2):
#            print(f"after  {mixed_gene[i]}, {mixed_gene[i+1]}")
#
#            sep = list((abs(mixed_gene[i][j]-mixed_gene[i+1][j]) for j in range(len(gene[0])))).index(1,1)
#            print(sep)
#            print(gene[i][:sep])
#            print(gene[i+1][sep:])
#
        pass


if __name__ == "__main__":
    unittest.main()

