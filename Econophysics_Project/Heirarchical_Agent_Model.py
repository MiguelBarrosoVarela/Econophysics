# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 15:23:24 2022

@author: Hugo Rauch
"""

import numpy as np
import matplotlib.pyplot as plt


#%%
#Initialisation

dt=0.1
sig=2.5
beta=4
rho=1.3
m=15
N=5
k=10
n=N-1#

def Hrarchy_Vect(i):
    vect=np.zeros(N,dtype=int)
    for l in range(N):# l=[0,1,...n]
        vect[l]=i//m**l
    return vect

def PDF(t,k,sig,rho):
    return k*sig**rho*np.exp(-k*sig**rho*t)*dt

def Cheat_PDF(t,k,sig,rho):
    return 0.1*np.exp(-sig)
    

#%%
#Performing iterations
t=0
Finish=0
times=np.array([])
sales=np.array([])
sigmas=sig*np.ones(m**n)
Hrarchy_Sold_Bool=np.zeros((N,m**n))
Hrarchy_Sold_Numbers=np.zeros((N,m**n))

while Finish==0:
    ##############################################
    UnsoldAgntsInds=np.array([],dtype=int)#Array with indices of unsold agents
    for i in range(m**n): #i are indices E[0,1,2,...m**n-1]
        if Hrarchy_Sold_Bool[0][i]==0:
            UnsoldAgntsInds=np.append(UnsoldAgntsInds,i)
    #This bit randomly picks of they sell during the timestep
    for i in UnsoldAgntsInds:
        Sigma=sigmas[i]
        Probability=PDF(t,k,Sigma,rho)*dt
        Random=np.random.rand()
        if Random<=Probability:#Randomly chooses whether to update
            Hrarchy_Sold_Bool[0][i]=1
            for HrarchyRow in range(N):#[0,1,2,...n]
                #HrarchyRow is heirarchy level we're dealing with
                Col=Hrarchy_Vect(i)[HrarchyRow]
                Col=int(Col)
                Hrarchy_Sold_Numbers[HrarchyRow][Col]+=1
    
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
        #This calculates new sigmas
        sigmas[i]=sig*2**(-S_vector[i]*beta/rho)  
        
    if t>=500:
        Finish=1
    
    ###############################################
    print(t)
    print(Hrarchy_Sold_Numbers[n][0])
    times=np.append(times,t)
    sales=np.append(sales,Hrarchy_Sold_Numbers[n][0])
    if Hrarchy_Sold_Bool[n][0]==1:
        Finish=1
    else:
        t+=dt
        
#%%
#plotting 
plt.plot(times,sales)