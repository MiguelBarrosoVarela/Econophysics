# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 16:14:50 2022

"""

import numpy as np
import matplotlib.pyplot as plt
import random

#%%
#Initialisation


sig=3
beta=0
rho=1
k=1
m=2#Number of subgroups per group
N=13#Number of levels in heirarchy including top layer with everyone
n=N-1#
agents=m**n



def Boost(x): # x is the array of times
  t=min(x) #find smallest time
  buyer=np.where(x == t)[0] #find index of buyer
  return(t,buyer)





#%%
#Performing iterations
S_vector_old=np.zeros(agents)
t=0#Initialising time
times=np.array([])#List of times where agents buy
sales=np.array([])#Sales at each time where agents buy
sigmas=sig*np.ones(agents)# List of sigma values for agents
S_vector=np.zeros(agents)#List of S values
Hrarchy_Sold_Bool=np.zeros((N,agents))


Split=0.5 # Approximate Starting Conditions: N_sellers/N_total

for i in range(agents):
    Hrarchy_Sold_Bool[0][i]=np.sign(random.random()-1+Split)
for i in range(1,N):
    for j in range(m**(n-i)):  #average matrix 
            Hrarchy_Sold_Bool[i][j]=sum(Hrarchy_Sold_Bool[i-1][j*m+k] for k in range(m))/m

            

"""
Need to initialise buy_time array - so first buy-time array

"""



TimeArray=np.array([-np.log(1-random.random())/(k*sig**rho) for i in range(agents)]) #Generate times from distribution
t,buyer=Boost(TimeArray)
t_old=t
#%%
BuyingPercentage=0.95 #Choose when the market is considered to be dominated

while abs(Hrarchy_Sold_Bool[n][0])<BuyingPercentage:
   
            
    t,buyer=Boost(TimeArray)  #Finds smallest time and the buyer index corresponding to that time
    if t/t_old>10:
        break #stops if the next time to buy is super super far (market dominated)
    t_old=t  
    
    Hrarchy_Sold_Bool[0][buyer]*=-1 #Flip the buyer/seller to seller/buyer
    
    #Getting averages matrix
    for i in range(1,N):
        for j in range(m**(n-i)):
            Hrarchy_Sold_Bool[i][j]=sum(Hrarchy_Sold_Bool[i-1][j*m+k] for k in range(m))/m
    

    
    #This calculates S value vector 
    S_vector=np.zeros(agents)
    for i in range(agents):
        S_vector[i]=sum(Hrarchy_Sold_Bool[j][int(i/(m**j))] for j in range(1,N))   
    #This calculates new_sigmas
        sign=np.sign(Hrarchy_Sold_Bool[0][i]) #determine which type of agent it is
        sigmas[i]=sig**rho*2**(-sign*S_vector[i]*beta)    

    
    for j in range(len(TimeArray)):
        if S_vector[j]==S_vector_old[j]:  #Does what is described above
            pass
        else: #generates new time using the new sigmas 
            TimeArray[j]=t-(np.log(1-random.random())/(k*sigmas[j]))
            

    ###############################################
    print(t)# Current time 
    SUM=sum(Hrarchy_Sold_Bool[0][j] for j in range(agents))
    print(SUM)#Total number of bought agents
    times=np.append(times,t)
    sales=np.append(sales,SUM)
    #plt.plot(times,sales,'k')    
    #plt.show()                     #in case you want to animate the market
    #plt.pause(0.0000001)             #this makes code slower of course
    S_vector_old=S_vector 

#%%        

salesAbs=[(sales[i]+agents)/(2*agents) for i in range(len(sales))]
plt.figure(0)
plt.ylim([min(salesAbs), max(salesAbs)])
plt.xlabel(r'Non-dimensional time ',size=15)
plt.ylabel('Stock Price',size=15) 
plt.fill_between(times,salesAbs,alpha=0.5)
plt.plot(times,salesAbs,label=r'$\sigma^{\rho}=$'+str(sig)+ r' , $\beta$= '+str(beta)+', N='+str(m**n)+r', Sold/Bought Fraction='+str(BuyingPercentage),color='black')
plt.legend(prop={"size":11})    
plt.grid(axis='y')
    

