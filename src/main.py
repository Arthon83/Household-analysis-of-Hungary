#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import logging

from moduls import Loader
from moduls import Simulation


# In[2]:


# List items [previous year, actual year, year[int]]
params= [
        ['2107_reconst.csv','2207_reconst.csv',2022],
        ['2207_reconst.csv','2307_reconst.csv',2023],
        ['2307_reconst.csv','2407_reconst.csv',2024],
       ]


# In[3]:


columns = ['PID', 'AGE', 'NEM', 'KSHIR', 'HT_TYPE']


# In[4]:


for data in params:
    left = Loader(data[0], columns, log_level = logging.INFO)
    left_df = left.load()

    right = Loader(data[1], columns)
    right_df = right.load()

    sim = Simulation(left_df, right_df, _id = 'PID', _dim = ['AGE_CAT','NEM','JOG'], _attr = 'HT_TYPE')
    merged_df = sim.preprocess(show_d = True)

    pivot_df, trans_prob = sim.get_transition_matrix(merged_df)
    trans_prob['YEAR'] = data[2]
    
    trans_prob.to_csv(f'{data[2]}_data.csv', index = False)
    pivot_df.to_csv(f'{data[2]}_pivot.csv', index = False)
    

