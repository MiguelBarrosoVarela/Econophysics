# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import optimize
#%%
#Initialisation


sig=3
beta=2
rho=1
k=1
m=2#Number of subgroups per group
N=8#Number of levels in heirarchy including top layer with everyone
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




#%%
tc=[]
TimeArrayOriginal=np.array([-np.log(1-random.random())/(k*sig**rho) for i in range(agents)]) #Generate times from distribution
tAvg=np.mean(TimeArrayOriginal)

simulations=1000
for trial in range(simulations):
  print(trial)
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
  TimeArray=np.array([TimeArrayOriginal[i] for i in range(len(TimeArrayOriginal))])
  while Hrarchy_Sold_Bool[n][0]==0:
   
            
    t,buyer=Boost(TimeArray)  #Finds smallest time and the buyer index corresponding to that time
    
    Hrarchy_Sold_Bool[0][buyer]=1
    for HrarchyRow in range(N):#[0,1,2,...n]
        #This updates the numerical Hrarchy matrix
        Hrarchy_Sold_Numbers[HrarchyRow][int(Hrarchy_Vect(buyer)[HrarchyRow])]+=1
    
    
    #Getting boolean Hrarchy matrix from numerical matrix
    for i in range(1,N):
        for j in range(m**(n-i)):
            if Hrarchy_Sold_Numbers[i][j]==m**i:
                Hrarchy_Sold_Bool[i][j]=1
    
    #Getting matrix to find S values
    Hrarchy_S=np.zeros((N,agents))#number of full n-1 order objcts in n ordr obj        
    Hrarchy_S[0]=Hrarchy_Sold_Numbers[0]
    Hrarchy_S[1]=Hrarchy_Sold_Numbers[1]
    for row in range(1,n):
        for i in range(0,m**(n-row)):
            if Hrarchy_S[row][i]==m:
                Hrarchy_S[row+1][i//m]+=1
    
    #This calculates S value vector 
    S_vector=np.zeros(agents)
    for i in range(agents):
        Vector_i=Hrarchy_Vect(i)
        S=0
        for j in range(1,N):
            S+=Hrarchy_S[j][Vector_i[j]]
        S_vector[i]=S    
    #This calculates new_sigmas
        sigmas[i]=sig**rho*2**(S_vector[i]*beta)    
    
   
    for j in range(len(TimeArray)):
        if S_vector[j]==S_vector_old[j] or TimeArray[j]==1e7:  #Does what is described above
            pass
        else: #generates new time using the new sigmas 
            TimeArray[j]=t-(np.log(1-random.random())/(k*sigmas[j]))
    
    ###############################################
    # Current time 
    #Total number of bought agents
    times=np.append(times,t)
    sales=np.append(sales,Hrarchy_Sold_Numbers[n][0])
    #plt.plot(times,sales,'k')    
    #plt.show()                     #in case you want to animate the market
    #plt.pause(0.00001)             #this makes code slower of course
    S_vector_old=S_vector 
    TimeArray[buyer]=1e7 #make sure this buyer never gets picked again by boost method
  
 
  tc.append(times[-1])        
#%%
#plotting 
plt.figure(0)
plt.xlabel(r'Time of Crash',size=15)
plt.ylabel('Number of Ocurrences',size=15) 
BINS=20
counts,bins,bars=plt.hist(tc,label=r'$<t_i>=$'+f'{tAvg:.3f}'+r', $\beta=$'+f'{beta:.2f}'+f', {simulations:.0f}'+' Simulations',density=False,bins=BINS)
plt.legend()    
centers=[(bins[i]+bins[i+1])/2 for i in range(BINS)]

ExpMean=centers[np.where(counts == np.max(counts))[0][0]]
def Gaussian(x,mean,sigma,A):
    return(A*np.exp(-(x-mean)**2/(2*sigma**2)))

Parameters,cov=optimize.curve_fit(Gaussian,centers,counts,p0=[ExpMean,np.std(tc),np.max(counts)])
error=np.sqrt(cov[0][0])

plt.plot(centers,Gaussian(centers,Parameters[0],Parameters[1],Parameters[2]),label=r'$\mu$='+f'{Parameters[0]:.3f}'+r' $\pm$'+f'{error:.3f}'+r', $\sigma=$ '+f'{Parameters[1]:.2f}'+', N='+f'{agents:.0f}')
plt.legend(prop={"size":11})   




