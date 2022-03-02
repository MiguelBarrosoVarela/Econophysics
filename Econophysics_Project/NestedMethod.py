# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 17:14:33 2022

"""
import numpy as np
import matplotlib.pyplot as plt
import random
#%%
k=1
sigma_rho=2 #sigma^rho
beta=2
Order=16 #number of levels of hierarchy

N=2**(Order-1)
times=[-np.log(1-random.random())/(k*sigma_rho) for i in range(N)] #Generate times from distribution
buy=[]
plt.figure(0)
plt.hist(times,bins=100)
#%%
def Crowd(t1,t2): #returns t12 given t1 and t2 (order is irrelevant)
    a=max(t1,t2)
    b=min(t1,t2)
    return(b+2**(-beta)*(a-b))

def HigherOrder(x): #returns order N+1 array of times from order N array of times using crowd effect
    n=len(x)
    y=[]
    for i in range(int(n/2)):
      y.append(Crowd(x[2*i],x[2*i+1]))
    return(y)
 
#%%   
TimeArray=[times]
for i in range(Order-1):  #Generates array of array of times for each order using crowd effect
    TimeArray.append(HigherOrder(TimeArray[i]))
    
for i in range(Order-1): #Descends to lowest order altering max times to the above order time
  for j in range(2**i): 
    MAX=max(TimeArray[Order-(i+2)][2*j],TimeArray[Order-(i+2)][2*j+1])
    g=TimeArray[Order-(i+2)].index(MAX)
    TimeArray[Order-(i+2)][g]=TimeArray[Order-(i+1)][j]


#%%
plt.figure(1)
plt.hist(TimeArray[0],bins=100) #Plots histogram of buying times

#%%
BuyList=[]
for i in range(len(TimeArray[0])):
    BuyList.append(i+1)  #Creates array [0,1,2,3,...] of Buyers
    
SortedTimes=TimeArray[0]
SortedTimes.sort()  #Creates array of sorted times
tc=np.mean(SortedTimes)  #estimates critical time as mean of buying times

LoggedTimes=[]
LoggedBuy=[]
j=1
for i in SortedTimes:
    
    if i<tc:
        LoggedTimes.append(np.log(tc-i)) #Log of difference from t to tc
        LoggedBuy.append(np.log(j/N))  #Log of fraction of buyers who have bought
        j+=1
    else: 
        break   
plt.figure(2)
plt.plot(SortedTimes,BuyList)

#plt.figure(3)
#plt.xlabel(r'log($t_c-t$)',size=15)
#plt.ylabel('Log(Buyers/N)',size=15)   #Plots logarithmic t-tc VS logarithmic buyers
#plt.gca().invert_xaxis()

#lt.plot(LoggedTimes,LoggedBuy)










    
    
    
    
    