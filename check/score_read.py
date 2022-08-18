#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 07:24:16 2022

@author: zotac
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("temp_score",header=None)
print(df)

plt.plot(np.arange(len(df[0])),df[0])
# plt.axis('scaled')
plt.show()