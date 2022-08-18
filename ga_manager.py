#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import random
import numpy as np
import os
from PIL import Image
from enum import Enum

import sim_loop as sl

CAR_NUM = 10

class GA_manager:
    def __init__(self):
        self.genes = []

    def debug_gene_content(self):
        for n,gene in enumerate(self.genes):
            print(f"{n},",end="")
            for i,g in enumerate(gene):
                if i % 8 == 0:
                    print("|",end="")
                print(f"{g}",end="")
            print("")

    def make_first_generation(self):
        for _ in range(CAR_NUM):
            self.genes.append([random.choice([1,0]) for _ in range(sl.GEN_NUM)])
        

    
    def get_gene(self, i):
        return self.genes[i]

    def choice_by_roulette(self, score_ga, choice_num):

        #得点を降順にソートしたもの
        work = sorted(score_ga,key=lambda x: x[1])
        score_sum = sum([w[0] for w in work])
    
        #得点が0から1になるように正規化
        sortScore = [w[0]/score_sum for w in work]
        # print(sortScore)
    
        #得点を区間に分割 各区間をtuple(開始,終了)にする
        bins = [0.0] + [sum(sortScore[:n+1]) for n in range(len(sortScore))]
        bins = [(bins[b0],bins[b0+1]) for b0 in range(len(bins)-1)]
        # print(bins)

        choices = []
        for i in range(choice_num):
            v = random.random()
            for n,(b0,b1) in enumerate(bins):
                if b0 <= v and v < b1:
                    choices.append(work[n])
        return choices

    def mix(self, ga_list):
        if len(ga_list) % 2 == 1:
            raise Exception("len(ga_list) is not even.")

        ga_length = len(ga_list[0])
        new_ga = []

        for i in range(0,len(ga_list),2):
            nx = random.randint(1,ga_length-1)
            #print(nx)
            new_ga.append(ga_list[i][:nx] + ga_list[i+1][nx:])
            new_ga.append(ga_list[i+1][:nx] + ga_list[i][nx:])
        return new_ga

    def mutation(self, ga_list, probability=0.3):
        ga_length = len(ga_list[0])
        new_ga = []

        for n,ga in enumerate(ga_list):
            if random.random() < probability:
                idx = random.randint(0,ga_length-1)
                if ga[idx] == 1:
                    ga[idx] = 0
                else:
                    ga[idx] = 1
            new_ga.append(ga)
        return new_ga
    
    def make_next_generation(self, score_ga):
        work = sorted(score_ga,key=lambda x: x[0],reverse=True)

        self.genes.clear()
        self.genes.append(work[0][1])
        self.genes.append(work[1][1])

        choices = self.choice_by_roulette(work,CAR_NUM-2)
        print("choices len:" + str(len(choices)))

        print([c[0] for c in choices])
        ga_list = [g[1] for g in choices]

        ga_list = self.mix(ga_list)
        ga_list = self.mutation(ga_list)
        self.genes += ga_list




