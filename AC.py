# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:13:12 2025

@author: Jaka
"""
import random

SEQ_LEN = 100
alphabet = ['A','B','C','D']
prob_dist = [0.5,0.3,0.1,0.1]

sequence = random.choices(alphabet, weights=prob_dist, k=SEQ_LEN)
print(''.join(sequence))