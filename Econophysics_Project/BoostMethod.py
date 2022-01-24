# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 14:41:24 2022

"""

import numpy as np
import matplotlib.pyplot as plt
import random
#%%
k=1
sigma_rho=2 #sigma^rho
beta=2
Order=14 #number of levels of hierarchy

N=2**(Order-1)
times=[-np.log(1-random.random())/(k*sigma_rho) for i in range(N)] #Generate times from distribution
buy=[]
for i in range(Order):
  buy.append(np.zeros(2**(Order-1-i)))  #for each level of hierarchy generate array of zeros of respective size


def Boost(x,n): #n is number of iteration, x is the array of times
  t=min(x) #find smallest time
  buyer=x.index(t)
  buy[0][buyer]=1
  if buyer%2==0 and x[buyer]>x[buyer+1] : #if buyer is even then affect odd next to him
    x[buyer+1]=x[buyer]+2**(-beta)*(x[buyer+1]-x[buyer])   
  elif buyer%2==1 and x[buyer]>x[buyer-1]: #if buyer is odd then affect even next to him
    x[buyer-1]=x[buyer]+2**(-beta)*(x[buyer-1]-x[buyer]) 
  x[buyer]=1e7 #make sure that this time is never considered again
  return(t,n+1)

TimeList=[]
ShareList=[]
for i in range(N):
    Hold=Boost(times,i) #run for all iterations
    TimeList.append(Hold[0])
    ShareList.append(Hold[1])
    

plt.xlabel('Time',size=15) #plot number of buyers vs time
plt.ylabel('Number of Buyers',size=15)
plt.plot(TimeList,ShareList)































