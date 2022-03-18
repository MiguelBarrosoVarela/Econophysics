# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 15:14:40 2022
"""

import numpy as np
import matplotlib.pyplot as plt
import random

#%%
#Initialisation


sig=3
beta=1.2
rho=1
k=1
m=5#Number of subgroups per group
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

length=400
height=length/N
plt.axes()
for i in range(N):
    
    for j in range(m**i):  
        rectangle = plt.Rectangle((j*length*m**(-i),height*i), length*m**(-i), height, fc='white',ec="black")
        plt.gca().add_patch(rectangle)


plt.axis('scaled')
plt.show()
filenumber=0
plt.savefig('Visualisation\Gif'+str(filenumber)+'.png')

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

"""
Need to initialise buy_time array - so first buy-time array

"""

TimeArray=np.array([-np.log(1-random.random())/(k*sig**rho) for i in range(agents)]) #Generate times from distribution


while Hrarchy_Sold_Bool[n][0]==0:
    filenumber+=1
            
    t,buyer=Boost(TimeArray)  #Finds smallest time and the buyer index corresponding to that time
    
    Hrarchy_Sold_Bool[0][buyer]=1
    rectangle = plt.Rectangle((buyer*length*m**(-n),height*n), length*m**(-n), height, fc='red',ec="black")
    plt.gca().add_patch(rectangle)
 
    
    for HrarchyRow in range(N):#[0,1,2,...n]
        #This updates the numerical Hrarchy matrix
        Hrarchy_Sold_Numbers[HrarchyRow][int(Hrarchy_Vect(buyer)[HrarchyRow])]+=1

    plt.savefig('Visualisation\Gif'+str(filenumber)+'.png')
    
    #Getting boolean Hrarchy matrix from numerical matrix
    for i in range(1,N):
        for j in range(m**(n-i)):
            if Hrarchy_Sold_Numbers[i][j]==m**i:
                Hrarchy_Sold_Bool[i][j]=1
                rectangle = plt.Rectangle((j*length*m**(-n+i),height*(n-i)), length*m**(-n+i), height, fc='red',ec="black")
                plt.gca().add_patch(rectangle)
                  
    plt.pause(1e-20)          
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
    times=np.append(times,t)
    sales=np.append(sales,Hrarchy_Sold_Numbers[n][0])
    #plt.plot(times,sales,'k')    
    #plt.show()                     #in case you want to animate the market
    #plt.pause(0.00001)             #this makes code slower of course
    S_vector_old=S_vector 
    TimeArray[buyer]=1e7 #make sure this buyer never gets picked again by boost method

filenumber+=1
plt.savefig('Visualisation\Gif'+str(filenumber)+'.png')



        

        
    