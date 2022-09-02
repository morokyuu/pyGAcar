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

STATE_T_NUM=3 # num of previous data
STATE_PATTERN = 4
STATE_NUM=STATE_PATTERN**STATE_T_NUM
ACTION_NUM=5*2 #speed:5bit * 2motor
GEN_NUM=ACTION_NUM * STATE_NUM # length of single gene

class GAManagerTest(unittest.TestCase):
    def setUp(self):
        print("setUp===")
        self.gm = gagm.GA_manager(GEN_NUM)

    def tearDown(self):
        pass

    def test_make_first_generation(self):
        self.gm.make_first_generation()
        #print(self.gm.genes)

        self.assertEqual(len(self.gm.genes),gagm.CAR_NUM)
        self.assertEqual(len(self.gm.genes[0]),GEN_NUM)

    def _score(self):
        return random.random()*100

    def test_choice_by_roulette(self):
        genes = []
        for i in range(gagm.CAR_NUM):
            g = list(int(b) for b in bin(2**(ACTION_NUM//2)+i)[3:]) 
            genes += [(self._score(),g)]

        genes = sorted(genes, key=lambda x: x[0], reverse=True)
        for gi in genes:
            print("{0:5.2f},{1}".format(gi[0],gi[1]))

        ga_1st = genes[0][1]
        ga_2nd = genes[1][1]
        print(genes[0][1])
        print(genes[1][1])

        count = 0
        for _ in range(100):
            choices = self.gm.choice_by_roulette(genes,2)
            #print(choices)
            if ga_1st == choices[0][1]:
                count += 1
            if ga_2nd == choices[1][1]:
                count += 1

        print("count={0}".format(count))
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

    def test_make_first_generation(self):
        genes = []
        for i in range(gagm.CAR_NUM):
            g = list(int(b) for b in bin(2**(ACTION_NUM//2)+i)[3:]) 
            genes += [(self._score(),g)]

        self.gm.make_next_generation(genes)


if __name__ == "__main__":
    unittest.main()

