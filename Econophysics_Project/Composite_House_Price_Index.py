# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 15:43:04 2022

@author: Hugo Rauch
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 18:19:15 2022

@author: Hugo Rauch
"""
"""https://fred.stlouisfed.org/series/SPCS20RSA"""

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

stock_values=np.loadtxt('SPCS20RSA.csv',skiprows=1,usecols=1,delimiter=',')
dates=np.linspace(0,len(stock_values)-1,len(stock_values),dtype=int)


#%%
"""Trying to load dates"""
true_dates=np.loadtxt('SPCS20RSA.csv',skiprows=1,usecols=0,delimiter=',',dtype=str)

#Removing days where stock_values=0
closed_market_dates=[]
for date in range(len(stock_values)):
    if stock_values[date]==0:
        closed_market_dates.append(date)
stock_values=np.delete(stock_values,closed_market_dates)
true_dates=np.delete(true_dates,closed_market_dates)
#Flipping stock values (in original data set recent values at top)
#stock_values=stock_values[::-1]   

plt.plot(dates,stock_values)
#%%
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in true_dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=500))
plt.plot(x,stock_values)
plt.gcf().autofmt_xdate()


#%%