# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:19:13 2022

@author: Hugo Rauch
"""
import Buy_only_simulation
import scipy.special as sc
import numpy as np
import matplotlib.pyplot as plt


def Analytic_time(x,beta,lam,agents):
    tc = 1/lam * 2**(-agents*beta) * sc.expi( np.log(2)*beta*agents )
    return tc - 1/lam * 2**(-beta*agents) * sc.expi( beta*np.log(2)  * (agents - x)   )

def Critical_time(beta,lam,agents):
    tc = 1/lam * 2**(-agents*beta) * sc.expi( np.log(2)*beta*agents )
    return tc
    

#%% Testing basic buy vs time

beta=0.04
lam=2
m=1000

n=np.arange(0,m,1)
t= Analytic_time(n, beta,lam, m)
Simulation(m,2,lam,beta,progress=True,plot=True)



plt.plot(t,n)


#%% Old module  
 
"""
def Analytic_time(x,beta,agents):
    return 2**(-beta*agents) * sc.expi( -beta*np.log(2)  * (x - agents) )-2**(-beta*agents) * sc.expi( -beta*np.log(2)  * (- agents) )
"""
n=np.arange(0,1000,1)
t= -Analytic_time(n, 0.03, 1000)
plt.figure(0)
plt.plot(t,n)
BuyOnlySimulation(1000,2,1,0.03,True,True)


#%%Old module
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
#%%New simulation for different beta values

beta=0.03
lam=2
m=5
N=5
agents=m**(N-1)
n=np.arange(0,m,1)

CriticalTimes=[]
PredictedCrit=[]
betaList=[]
n=np.arange(0,agents,1)
for i in np.linspace(0,0.03,100):
    betaList.append(i)
    times,sales=Simulation(m,N,lam,beta)
    CriticalTimes.append(times[-1])
    tc=Critical_time(beta,lam,agents)
    PredictedCrit.append(tc)
    
plt.plot(betaList,CriticalTimes)


#%%

#Plot predicted and simulated tc VS beta
plt.figure(3)
plt.xlabel(r'$\beta$')
plt.ylabel('Critical Time')     
plt.plot(np.linspace(0.01,0.03,100),CriticalTimes,'o')  
plt.plot(np.linspace(0.01,0.03,100),PredictedCrit)  