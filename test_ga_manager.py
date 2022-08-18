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

class GAManagerTest(unittest.TestCase):
    def setUp(self):
        print("setUp===")
        self.gm = gagm.GA_manager()

    def tearDown(self):
        pass

    def test_make_first_generation(self):
        self.gm.make_first_generation()
        print(self.gm.genes)
        self.assertEqual(0,0)



if __name__ == "__main__":
    unittest.main()

