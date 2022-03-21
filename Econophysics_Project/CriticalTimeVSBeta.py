# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 14:00:57 2022
"""

import Buy_only_simulation as BOS
import matplotlib.pyplot as plt
import numpy as np


BetaRange=np.linspace(0.5,2,30)
CriticalTimes=[[] for i in range(3)]
count=0
for j in range(2,5,1):
 
 for i in BetaRange:
    times,sales=BOS.BuyOnlySimulation(m=j,N=9,lam=2,beta=i)
    CriticalTimes[count].append(times[-1])
    print(i)
 count+=1
 print(j)   
#%%
for j in range(3):   
    plt.figure(1)
    plt.xlabel(r'$\beta$',size=15)
    plt.ylabel('Critical Time',size=15)
    plt.plot(BetaRange,CriticalTimes[j],label='N=8,'+'m='+str(j+2))
plt.legend(prop={"size":11})
#%%
import scipy.special as sc

def Criti(beta,m=3):
    return(1/2 * 2**(-m*beta) * sc.expi( np.log(2)*beta*m ))

plt.plot(BetaRange,Criti(beta=BetaRange,m=2),label='Analytical Critical Time for m=2')

