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
beta=0.02
rho=1
k=1
m=2#Number of subgroups per group
N=10#Number of levels in heirarchy including top layer with everyone
n=N-1#
agents=m**n



def Boost(x): # x is the array of times
  t=min(x) #find smallest time
  buyer=np.where(x == t)[0] #find index of buyer
  return(t,buyer)

def Hrarchy_Vect(i):
    vect=np.zeros(N,dtype=int)
    for l in range(N):# l=[0,1,...n]
        vect[l]=i//m**l
    return vect




#%%
#Performing iterations
S_vector_old=np.zeros(agents)
Change_Times_List=[]
t=0#Initialising time
Finish=0
times=np.array([])#List of times where agents buy
sales=np.array([])#Sales at each time where agents buy
sigmas=sig*np.ones(m**n)# List of sigma values for agents
S_vector=np.zeros(m**n)#List of S values
Hrarchy_Sold_Bool=np.zeros((N,agents))
Hrarchy_Sold_Numbers=np.zeros((N,agents))

Split=0.5 # Approximate Starting Conditions: N_sellers/N_total

for i in range(agents):
    Hrarchy_Sold_Bool[0][i]=np.sign(random.random()-1+Split)
for i in range(1,N):
    for j in range(m**(n-i)):
            Hrarchy_Sold_Bool[i][j]=sum(Hrarchy_Sold_Bool[i-1][j*m+k] for k in range(m))/m

            

"""
Need to initialise buy_time array - so first buy-time array

"""


TimeArray=np.array([-np.log(1-random.random())/(k*sig**rho) for i in range(agents)]) #Generate times from distribution
#%%

while abs(Hrarchy_Sold_Bool[n][0])!=1:
    ##############################################
    
    #This bit creates list of indices of agents who haven't sold
    #This could be streamlined with new boost method, but we'll do that later. 
    
    # UnsoldAgntsInds=np.array([],dtype=int)
    # for i in range(m**n):
    #     if Hrarchy_Sold_Bool[0][i]==0:
    #         UnsoldAgntsInds=np.append(UnsoldAgntsInds,i)
            
    t,buyer=Boost(TimeArray)  #Finds smallest time and the buyer index corresponding to that time
    
    
    Hrarchy_Sold_Bool[0][buyer]*=-1
    
    #Getting boolean Hrarchy matrix from numerical matrix
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
    
    """
    Generate new buy times
    ----------------------
    
    S_vector is the list of S values for the agents. E.g. S_vector[3] is the S
    value for the agent with index 3. Perhaps store the previous s vector and 
    compare this to the current S_vector. 
    
    For the agents with changed S_vector values, generate new times. Use the 
    PDF to generate dt. Then add dt to t (which is the time of this iteration)
    - this is their new buy time. 

    

    """
    
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
    plt.plot(times,sales,'k')    
    plt.show()                     #in case you want to animate the market
    plt.pause(0.0000001)             #this makes code slower of course
    S_vector_old=S_vector 
    #make sure this buyer never gets picked again by boost method
  
    #t+=dt, assumed this bit is no longer needed as no longer using FD method
#%%        
plt.figure(0)
plt.xlabel(r'Non-dimensional time ',size=15)
plt.ylabel('Buyers',size=15) 

plt.plot(times,sales,label=r'$\sigma^{\rho}=$'+str(sig)+ r' , $\beta$= '+str(beta)+', N='+str(m**n))
plt.legend()    
        
    

