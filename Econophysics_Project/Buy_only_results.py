# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 11:01:56 2022

@author: Hugo Rauch
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:19:13 2022

@author: Hugo Rauch
"""
import Buy_only_simulation
import scipy.special as sc
import numpy as np
import matplotlib.pyplot as plt

#%%Different buy-time curves

#1-layer
Buy_only_simulation.BuyOnlySimulation(100,2,1,0.1,True,True,True)

#Normal hierarchy
Buy_only_simulation.BuyOnlySimulation(6,5,1e-7,3,True,True,True)

#Nuclear decay
Buy_only_simulation.BuyOnlySimulation(100,2,1,0,True,True,True)

#%%