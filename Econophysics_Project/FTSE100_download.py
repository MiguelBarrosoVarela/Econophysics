# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:01:59 2022

@author: Hugo Rauch

Data Source
-----------

https://www.wsj.com/market-data/quotes/index/UK/UKX/historical-prices


"""
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit

stock_values=np.loadtxt('HistoricalPricesFTSE100.csv',skiprows=1,usecols=1,delimiter=',')
dates=np.linspace(0,len(stock_values)-1,len(stock_values),dtype=int)


#%%
"""Trying to load dates"""
true_dates=np.loadtxt('HistoricalPricesFTSE100.csv',skiprows=1,usecols=0,delimiter=',',dtype=str)

#Removing days where stock_values=0
closed_market_dates=[]
for date in range(len(stock_values)):
    if stock_values[date]==0:
        closed_market_dates.append(date)
stock_values=np.delete(stock_values,closed_market_dates)
true_dates=np.delete(true_dates,closed_market_dates)
#Flipping stock values (in original data set recent values at top)
#stock_values=stock_values[::-1]   



x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in true_dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=500))
plt.plot(x,stock_values)
plt.gcf().autofmt_xdate()

#%%
"""Fitting the curve to the graph"""


plt.plot(x,stock_values)

"""600 to 1660 is a good range of points to plot to the curve"""

#stock_values=stock_values[::-1]   
fit_dates=dates[600:1660]
fit_prices=stock_values[600:1660]
#plt.plot(fit_dates,fit_prices)

def LogPeriodic(t,tc,a,w,C,A,B,P):
    return A+B*(tc-t)**a*(1 + C*np.cos(w*np.log(t-tc) +P))

popt, pcov = curve_fit(LogPeriodic, fit_dates, fit_prices,p0=[1660,1,1/50,4000,1000,1000,1000], maxfev=5000)



