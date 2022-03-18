# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 10:56:23 2022

@author: Hugo Rauch
"""

"""https://finance.yahoo.com/quote/%5EGSPC/history?period1=486432000&period2=581126400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"""

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit

#Loading the value of stocks
stock_values=np.loadtxt('SPX_87_crash_yahoo_finance.csv',skiprows=1,usecols=1,delimiter=',')
#List of indices of stock values
dates=np.linspace(0,len(stock_values)-1,len(stock_values),dtype=float)
#Loading the true dates
true_dates=np.loadtxt('SPX_87_crash_yahoo_finance.csv',skiprows=1,usecols=0,delimiter=',',dtype=str)

#Removing days where stock_values=0
closed_market_dates=[]
for date in range(len(stock_values)):
    if stock_values[date]==0:
        closed_market_dates.append(date)
stock_values=np.delete(stock_values,closed_market_dates)
true_dates=np.delete(true_dates,closed_market_dates)


#Flipping stock values (in original data set recent values at top)
#Only relevant for idices as dates. 
#stock_values=stock_values[::-1]   

#fit_times=dates[14606:14800]
#fit_prices=stock_values[14606:14800]
#plt.plot(fit_times,fit_prices)


def LogPeriodic(t,tc,a,w,C,A,B,P):
    return A+(B*(tc-t)**a)*(1 + C*np.cos(w*np.log(tc-t) + P))

#%% Plotting index against dates
x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in true_dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5000))
#plt.plot(x,stock_values)
plt.gcf().autofmt_xdate()
#%% Performing fit 
stock_values=stock_values[::-1]   
#100 to 560 is the best range
upper_bound=560
lower_bound=100
fit_labels=dates[lower_bound:upper_bound]
fit_dates=(fit_labels-lower_bound)/(upper_bound-lower_bound)*(87.5-85.5)+85.5
fit_stocks=stock_values[lower_bound:upper_bound]


#Performing the actual fit

parameters=[87.74,0.33,7.4,12.2/-165,412,-165,2]
popt, pcov = curve_fit(LogPeriodic,fit_dates,fit_stocks, parameters, maxfev=5000)
ydata=LogPeriodic(fit_dates,*popt)
#plt.plot(fit_labels,fit_stocks)
#plt.plot(fit_labels,ydata)
#%%Plotting fit against dates
#Take care with the data flipping

x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in true_dates][lower_bound:upper_bound]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=140))
plt.plot(x,fit_stocks[::-1],color='black',label='Stock Market Data')
plt.gcf().autofmt_xdate()
plt.plot(x,ydata[::-1],color='red',label='Log-Periodic Fit')
plt.fill_between(x,fit_stocks[::-1],alpha=0.5)
plt.ylim([min(fit_stocks), max(fit_stocks)])
plt.rc('xtick', labelsize=12) 
plt.legend(prop={"size":11})    
plt.grid(axis='y')
plt.xlabel('Date',size=17)
plt.ylabel('S&P 500 value',size=15)
