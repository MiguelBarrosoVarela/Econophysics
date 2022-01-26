# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 17:46:20 2022

@author: Hugo Rauch
"""
import numpy as np
import matplotlib.pyplot as plt


#%%
#Initialisation

dt=0.001
sig=0.1
beta=1.1
rho=1
k=1
m=15#Number of subgroups per group
N=5#Number of levels in heirarchy including top layer with everyone
n=N-1#

def Hrarchy_Vect(i):
    vect=np.zeros(N,dtype=int)
    for l in range(N):# l=[0,1,...n]
        vect[l]=i//m**l
    return vect

def PDF(t,k,sig,rho):
    return k*sig**rho*np.exp(-k*sig**rho*t)*dt

def Buy_Probability(s,k=k,sig=sig,rho=rho,beta=beta,dt=dt):
    return k*sig**rho*2**(beta*s)*dt

#%%
#Performing iterations
S_vector_old=np.zeros(m**n)
Change_Times_List=[]
t=0#Initialising time
Finish=0
times=np.array([])#List of times where agents buy
sales=np.array([])#Sales at each time where agents buy
sigmas=sig*np.ones(m**n)# List of sigma values for agents
S_vector=np.zeros(m**n)#List of S values
Hrarchy_Sold_Bool=np.zeros((N,m**n))
Hrarchy_Sold_Numbers=np.zeros((N,m**n))

"""
Need to initialise buy_time array - so first buy-time array

"""

while Finish==0:
    ##############################################
    
    #This bit creates list of indices of agents who haven't sold
    #This could be streamlined with new boost method, but we'll do that later. 
    UnsoldAgntsInds=np.array([],dtype=int)
    for i in range(m**n):
        if Hrarchy_Sold_Bool[0][i]==0:
            UnsoldAgntsInds=np.append(UnsoldAgntsInds,i)
            
    
    """
    Boost
    -----
    
    List/Array of buy_times from previous iteration or initialisation) known. 
    From list of indices of unsold agents, find smallest time t'. 
    t=t', append this to times array. 
    
    Index of agent with buy time t' is i. Then assert that this guy has sold 
    using:
        
    Hrarchy_Sold_Bool[0][i]=1
    for HrarchyRow in range(N):#[0,1,2,...n]
        #This updates the numerical Hrarchy matrix
        Column=Hrarchy_Vect(i)[HrarchyRow]
        Column=int(Column)
        Hrarchy_Sold_Numbers[HrarchyRow][Column]+=1
    
    Now the code knows this guy has sold. Continue with the origianl code: 
    """
    
    #Getting boolean Hrarchy matrix from numerical matrix
    for i in range(1,N):
        for j in range(m**(n-i)):
            if Hrarchy_Sold_Numbers[i][j]==m**i:
                Hrarchy_Sold_Bool[i][j]=1
    
    #Getting matrix to find S values
    Hrarchy_S=np.zeros((N,m**n))#number of full n-1 order objcts in n ordr obj        
    Hrarchy_S[0]=Hrarchy_Sold_Numbers[0]
    Hrarchy_S[1]=Hrarchy_Sold_Numbers[1]
    for row in range(1,n):
        for i in range(0,m**(n-row)):
            if Hrarchy_S[row][i]==m:
                Hrarchy_S[row+1][i//m]+=1
    
    #This calculates S value vector 
    S_vector=np.zeros(m**n)
    for i in range(m**n):
        Vector_i=Hrarchy_Vect(i)
        S=0
        for j in range(1,N):
            S+=Hrarchy_S[j][Vector_i[j]]
        S_vector[i]=S    
    #This calculates new_sigmas
        sigmas[i]=sig*2**(-S_vector[i]*beta/rho)    
    
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
    
    ###############################################
    print(t)# Current time 
    print(Hrarchy_Sold_Numbers[n][0])#Total number of bought agents
    times=np.append(times,t)
    sales=np.append(sales,Hrarchy_Sold_Numbers[n][0])
    S_vector_old=S_vector 
    if Hrarchy_Sold_Bool[n][0]==1:
        Finish=1
    else:
        t+=dt
        
#%%
#plotting 
plt.plot(times,sales)
        


        
        
    

