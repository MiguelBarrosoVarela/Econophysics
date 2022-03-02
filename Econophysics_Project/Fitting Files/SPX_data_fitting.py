# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 16:00:58 2022

@author: Hugo Rauch
"""

"""Data loading and imports"""

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

stock_values=np.loadtxt('HistoricalData_1644422317059.csv',skiprows=1,usecols=3,delimiter=',')
dates=np.linspace(0,len(stock_values)-1,len(stock_values),dtype=int)


#%%
"""Trying to load dates"""
true_dates=np.loadtxt('HistoricalData_1644422317059.csv',skiprows=1,usecols=0,delimiter=',',dtype=str)

#Removing days where stock_values=0
closed_market_dates=[]
for date in range(len(stock_values)):
    if stock_values[date]==0:
        closed_market_dates.append(date)
stock_values=np.delete(stock_values,closed_market_dates)
true_dates=np.delete(true_dates,closed_market_dates)
#Flipping stock values (in original data set recent values at top)
#stock_values=stock_values[::-1]   



x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in true_dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=500))
plt.plot(x,stock_values)
plt.gcf().autofmt_xdate()


#%%


"""
n-day moving chi_sq value
--------------------------

Divide dates into chunks of n days
Takes stock values and dates in that chunk
Fits log-periodic curve
Calculates chisq
plots chisq against time

"""

n=30#chunk size

current_chunk=0
current_lb=0
current_ub=30

chunk_dates=dates[0:30]
chunk_prices=stock_values[0:30]








    
    