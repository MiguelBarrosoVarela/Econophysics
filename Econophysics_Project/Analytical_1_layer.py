# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:19:13 2022

@author: Hugo Rauch
"""
import Buy_only_simulation
import scipy.special as sc
import numpy as np
import matplotlib.pyplot as plt

def Analytic_time(x,beta,agents):
    return 2**(-beta*agents) * sc.expi( -beta*np.log(2)  * (x - agents)   )

n=np.arange(0,625,1)
t= -Analytic_time(n, 1.3, 625)

plt.plot(t,n)