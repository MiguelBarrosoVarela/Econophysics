# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:19:13 2022

@author: Hugo Rauch
"""
import Buy_only_simulation as BOS
import scipy.special as sc
import numpy as np
import matplotlib.pyplot as plt

def Analytic_time(x,beta,agents):
    return 2**(-beta*agents) * sc.expi( -beta*np.log(2)  * (x - agents) )-2**(-beta*agents) * sc.expi( -beta*np.log(2)  * (- agents) )

n=np.arange(0,1000,1)
t= -Analytic_time(n, 0.03, 1000)
plt.figure(0)
plt.plot(t,n)
BOS.BuyOnlySimulation(1000,2,1,0.03,True,True)


#%%
#Run simulation for different values of beta
CriticalTimes=[]
PredictedCrit=[]
n=np.arange(0,500,1)
for i in np.linspace(0.01,0.03,100):
     times,sales=BOS.BuyOnlySimulation(500,2,1,i)
     CriticalTimes.append(times[-1])
     t= -Analytic_time(n, i, 500)
     PredictedCrit.append(t[-1])
     print(i)
#%%

#Plot predicted and simulated tc VS beta
plt.figure(3)
plt.xlabel(r'$\beta$')
plt.ylabel('Critical Time')     
plt.plot(np.linspace(0.01,0.03,100),CriticalTimes,'o')  
plt.plot(np.linspace(0.01,0.03,100),PredictedCrit)  