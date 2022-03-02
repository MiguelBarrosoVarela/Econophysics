# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
import random
#%%
sig=3
beta=4
rho=1
k=1
m=2#Number of subgroups per group
N=12#Number of levels in heirarchy including top layer with everyone
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
times=[np.array([0]) for i in range(N)]
sales=[np.array([0]) for i in range(N)]
times1=np.array([0])#List of times where agents buy
sales1=np.array([0])#Sales at each time where agents buy
sigmas=sig*np.ones(m**n)# List of sigma values for agents
S_vector=np.zeros(m**n)#List of S values
Hrarchy_Sold_Bool=np.zeros((N,agents))
Hrarchy_Sold_Numbers=np.zeros((N,agents))
times0=np.array([])
sales0=np.array([])

TimeArray=np.array([-np.log(1-random.random())/(k*sig**rho) for i in range(agents)]) #Generate times from distribution


while Hrarchy_Sold_Bool[n][0]==0:
    ##############################################
    
    #This bit creates list of indices of agents who haven't sold
    #This could be streamlined with new boost method, but we'll do that later. 
    
    # UnsoldAgntsInds=np.array([],dtype=int)
    # for i in range(m**n):
    #     if Hrarchy_Sold_Bool[0][i]==0:
    #         UnsoldAgntsInds=np.append(UnsoldAgntsInds,i)
            
    t,buyer=Boost(TimeArray)  #Finds smallest time and the buyer index corresponding to that time
    
    Hrarchy_Sold_Bool[0][buyer]=1
    for HrarchyRow in range(N):#[0,1,2,...n]
        #This updates the numerical Hrarchy matrix
        Hrarchy_Sold_Numbers[HrarchyRow][int(Hrarchy_Vect(buyer)[HrarchyRow])]+=1
    
    for row in range(n):
      if Hrarchy_Sold_Numbers[row+1][buyer//(m**(row+1))]==m**(row+1):
        sales[row+1]=np.append(sales[row+1],sales[row+1][-1]+1)
        times[row+1]=np.append(times[row+1],t)
    
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
    print(t)# Current time 
    print(Hrarchy_Sold_Numbers[n][0])#Total number of bought agents
    times[0]=np.append(times[0],t)
    sales[0]=np.append(sales[0],Hrarchy_Sold_Numbers[n][0])
    #plt.plot(times,sales,'k')    
    #plt.show()                     #in case you want to animate the market
    #plt.pause(0.00001)             #this makes code slower of course
    S_vector_old=S_vector 
    TimeArray[buyer]=1e7 #make sure this buyer never gets picked again by boost method
  
    #t+=dt, assumed this bit is no longer needed as no longer using FD method
        
#%%
#plotting 
plt.figure(0)
plt.title('Scale Invariance', size=18)
plt.xlabel(r'Non-dimensional time ',size=15)
plt.ylabel('Order 0 Buyers',size=15) 

plt.plot(times[0],sales[0],label=r'$\sigma^{\rho}=$'+str(sig)+ r' , $\beta$= '+str(beta)+', N='+str(m**n))
plt.legend()    
#%%
plt.figure(1)
plt.title('Scale Invariance', size=18)
plt.xlabel(r'Non-dimensional time ',size=15)
plt.ylabel('Order 1 Buyers',size=15) 

plt.plot(times[1],sales[1],label=r'$\sigma^{\rho}=$'+str(sig)+ r' , $\beta$= '+str(beta)+', N='+str(m**n))
plt.legend() 
#%%
plt.figure(3)
plt.xlabel(r'Non-dimensional time ',size=15)
plt.ylabel('Scaled Buyers',size=15) 


for i in range(4):
   plt.plot(times[i],sales[i]*(m**i),label=r'Scaled Order '+f'{i}'+r' Buyers, $\sigma^{\rho}=$'+str(sig)+ r' , $\beta$= '+str(beta)+', N='+str(m**(n-i)))

plt.legend(prop={"size":11})    




#%%
LogTimes=[]
LogSales=[]
#Log Plotting
for i in range(4):
    tc=times[0][-1]
    LoggedTimes=[]
    LoggedSales=[]
    for j in range(len(times[i])-2):
      t=times[i][j+1]   
      LoggedTimes.append(np.log(tc-t))
      LoggedSales.append(np.log(sales[i][j+1]*(m**i)))
    LogTimes.append(LoggedTimes)
    LogSales.append(LoggedSales)
plt.figure(2)
plt.gca().invert_xaxis()
plt.xlabel(r'log($t_c-t$)',size=15)
plt.ylabel('Log(Scaled Buyers)',size=15) 

for i in range(4):   
    plt.plot(LogTimes[i],LogSales[i],label=r'Log of Scaled Order '+f'{i}'+r' Buyers, $\sigma^{\rho}=$'+str(sig)+ r' , $\beta$= '+str(beta)+', N='+str(m**(n-i)))

plt.legend(prop={"size":11})   





        