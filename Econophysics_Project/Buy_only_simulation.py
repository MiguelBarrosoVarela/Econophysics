# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 17:46:20 2022

@author: Hugo Rauch
"""
import numpy as np
import matplotlib.pyplot as plt
import random


def Boost(x): # x is the array of times
  t=min(x) #find smallest time
  buyer=np.where(x == t)[0] #find index of buyer
  return(t,buyer)

def Hrarchy_Vect(i,N,m):
    vect=np.zeros(N,dtype=int)
    for l in range(N):# l=[0,1,...n]
        vect[l]=i//m**l
    return vect



#%%Turning it into a function
def BuyOnlySimulation(m,N,lam,beta,progress=False,plot=False,fraction_plot=False):

    """

    Parameters
    ----------
    m : Number of subgroups per group
    N : Number of levels in the hierarchy (includes top layer with the group which contains all agents)
    lam : Exponent in PDF
    beta : Imitation parameter
    plot : Bool,
        Should the function be plotted? The default is False.
    progress : Bool,
        Should % completion be printed? The default is False.

    Returns
    -------
    Returns tuple (times,sales), where times is an array of buy times, and sales is an array of the numer of people who have bought at time t

    """    

    
    #%%#Initialisation
    
    sig=lam
    rho=1
    k=1
    n=N-1#
    agents=m**n
        
    #%%#Performing iterations
    
    S_vector_old=np.zeros(agents)
    t=0#Initialising time
    times=np.array([])#List of times where agents buy
    sales=np.array([])#Sales at each time where agents buy
    sigmas=sig*np.ones(m**n)# List of sigma values for agents
    S_vector=np.zeros(m**n)#List of S values
    Hrarchy_Sold_Bool=np.zeros((N,agents))
    Hrarchy_Sold_Numbers=np.zeros((N,agents))

    
    TimeArray=np.array([-np.log(1-random.random())/(k*sig**rho) for i in range(agents)]) #Generate times from distribution
    
    
    while Hrarchy_Sold_Bool[n][0]==0:
        ##############################################
        
                
        t,buyer=Boost(TimeArray)  #Finds smallest time and the buyer index corresponding to that time
            
        
        #Finds the new numerical Hrarchy matrix 
        for HrarchyRow in range(N):#[0,1,2,...n]
            Hrarchy_Sold_Numbers[HrarchyRow][int(Hrarchy_Vect(buyer,N,m)[HrarchyRow])]+=1
    
        #Getting boolean Hrarchy matrix from numerical matrix
        for i in range(0,N):
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
            Vector_i=Hrarchy_Vect(i,N,m)
            S=0
            for j in range(1,N):
                S+=Hrarchy_S[j][Vector_i[j]]
            S_vector[i]=S  
            
        #This calculates new_sigmas
            sigmas[i]=sig**rho*2**(S_vector[i]*beta)    
        
        #Generates new times 
        #Only for agents with S calues which changed this turn
        for j in range(len(TimeArray)):
            if S_vector[j]==S_vector_old[j] or TimeArray[j]==1e7:  
                pass
            else: #generates new time using the new sigmas 
                TimeArray[j]=t-(np.log(1-random.random())/(k*sigmas[j]))
        
        #Progress percentage, and storing of time and sales
        if progress==True:
            print(100*Hrarchy_Sold_Numbers[n][0]/agents,'% complete')           
        times=np.append(times,t)
        sales=np.append(sales,Hrarchy_Sold_Numbers[n][0])
        #plt.plot(times,sales,'k')    
        #plt.show()                     #in case you want to animate the market
        #plt.pause(0.00001)             #this makes code slower of course
        S_vector_old=S_vector 
        TimeArray[buyer]=1e7 #make sure this buyer never gets picked again by boost method
      
        #t+=dt, assumed this bit is no longer needed as no longer using FD method
            
    if plot==True:
        
        #plotting 
        plt.figure(0)
        plt.xlabel(r'Non-dimensional time ',size=15)
        plt.ylabel('Buyers',size=15) 
        
        if fraction_plot==True:
            plt.plot(times/times[-1],sales/sales[-1],label= r'$\beta$= '+str(beta)+', N='+str(N)+' m='+str(m),linewidth=2)      
        else:
            plt.plot(times,sales,label= r'$\beta$= '+str(beta)+', N='+str(N)+'m='+str(m),linewidth=2)
        
        
        plt.legend(prop={"size":11})   
        plt.grid(True)
        
        #Log Plotting
        tc=times[-1]
        LoggedTimes=[]
        for j in times:
            if j<tc:
                LoggedTimes.append(np.log(tc-j))
        
        plt.figure(2)
        plt.gca().invert_xaxis()
        plt.xlabel(r'log($t_c-t$)',size=15)
        plt.ylabel('Log(Buyers)',size=15) 
        plt.plot(LoggedTimes,np.log(sales[:len(LoggedTimes):]),color='black')
        plt.grid(True)
        
    return (times,sales)

