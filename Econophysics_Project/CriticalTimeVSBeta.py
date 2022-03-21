# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 14:00:57 2022
"""

import Buy_only_simulation as BOS
import matplotlib.pyplot as plt
import numpy as np

CriticalTimes=[]
for i in np.linspace(1,6,100):
    times,sales=BOS.BuyOnlySimulation(2,10,2,i)
    CriticalTimes.append(times[-1])
    print(i)

plt.plot(np.linspace(1,6,0.05),CriticalTimes)