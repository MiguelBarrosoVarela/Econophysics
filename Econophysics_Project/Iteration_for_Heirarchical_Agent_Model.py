# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 14:47:40 2022

@author: Hugo Rauch
"""

import numpy as np
import matplotlib.pyplot as plt


#%%
#Initialisation

dt=0.01
sig=1
beta=2
rho=1
m=2
N=5
k=1
n=N-1


S_vector_old=np.zeros(m**n)
Change_Times_List=[]
S_vector=np.zeros(m**n)
sigmas=sig*np.ones(m**n)
new_sigmas=sig*np.ones(m**n)
Hrarchy_Sold_Bool=np.zeros((N,m**n))
Hrarchy_Sold_Numbers=np.zeros((N,m**n))


for i in range(m**n):
    Change_Times_List.append([])    

def Hrarchy_Vect(i):
    vect=np.zeros(N,dtype=int)
    for l in range(N):# l=[0,1,...n]
        vect[l]=i//m**l
    return vect

def PDF(t,k,sig,rho):
    return k*sig**rho*np.exp(-k*sig**rho*t)

def Buy_Probability(s,dt=dt,k=k,sig=sig,rho=rho,beta=beta):
    return k*sig**rho*2**(beta*s)*dt

t=0#initialisation
#%%
#Basic Loop Code


#This makes an array of indices of agents who haven't sold this turn
UnsoldAgntsInds=np.array([],dtype=int)
for i in range(m**n): #i are indices E[0,1,2,...m**n-1]
    if Hrarchy_Sold_Bool[0][i]==0:
        UnsoldAgntsInds=np.append(UnsoldAgntsInds,i)
#This bit randomly picks if unsold agents sell during the timestep
for i in UnsoldAgntsInds:
    Sigma=sigmas[i]
    Probability=Buy_Probability(S_vector_old[i],dt)
    Random=np.random.rand()
    if Random<=Probability:#Randomly chooses whether to update
#If they sell, this bit updates the numerical matrix        
        Hrarchy_Sold_Bool[0][i]=1        
        for HrarchyRow in range(N):#[0,1,2,...n]
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
#This calculates new_sigmas
    
    sigmas[i]=sig*2**(-S_vector[i]*beta/rho)    

#This checks to see if an agent's s value has changed. 
#If it has, it will add the time to its time matrix. UNLESS t=0.
for i in UnsoldAgntsInds:
    if S_vector_old[i]!=S_vector[i]:
        Change_Times_List[i].append(t)

#This changes S_vector_old to S vector
S_vector_old=S_vector
t+=1

print(Hrarchy_Sold_Numbers[0])    
print(Change_Times_List)
#print(Hrarchy_S)            
print(S_vector)
#print(sigmas)

        


        
        
    


