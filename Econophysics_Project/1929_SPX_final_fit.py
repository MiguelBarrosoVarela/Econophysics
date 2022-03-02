# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 18:46:17 2022

@author: Hugo Rauch
"""
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit

#Loading the value of stocks
stock_values=np.loadtxt('SPX_29_crash_Yahoo_finance.csv',skiprows=1,usecols=1,delimiter=',')
#List of indices of stock values
dates=np.linspace(0,len(stock_values)-1,len(stock_values),dtype=float)
#Loading the true dates
true_dates=np.loadtxt('SPX_29_crash_Yahoo_finance.csv',skiprows=1,usecols=0,delimiter=',',dtype=str)

#Removing days where stock_values=0
closed_market_dates=[]
for date in range(len(stock_values)):
    if stock_values[date]==0:
        closed_market_dates.append(date)
stock_values=np.delete(stock_values,closed_market_dates)
true_dates=np.delete(true_dates,closed_market_dates)


def LogPeriodic(t,tc,a,w,C,A,B,P):
    return A+(B*(tc-t)**a)*(1 + C*np.cos(w*np.log(tc-t) + P))


#%% Plotting index against dates
x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in true_dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5000))
plt.plot(x,stock_values)
plt.gcf().autofmt_xdate()
#%% Plotting against number

plt.plot(dates,stock_values[::-1])
#0 to 425 are the best

#%% Performing fit 

 
#100 to 560 is the best range
#28 to 29.75 in dates
upper_bound=425
lower_bound=0
fit_labels=dates[lower_bound:upper_bound]
fit_dates=(fit_labels-lower_bound)/(upper_bound-lower_bound)*(29.75-28)+28
fit_stocks=stock_values[::-1][lower_bound:upper_bound]


parameters=[30.22,0.45,7.9,14.3/-267,5710,-2670,1]
popt, pcov = curve_fit(LogPeriodic,fit_dates,fit_stocks, parameters, maxfev=5000)
ydata=LogPeriodic(fit_dates,*popt)
plt.plot(fit_labels,fit_stocks)
plt.plot(fit_labels,ydata)
#%%Plotting fit against dates
#Take care with the data flipping

x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in true_dates][lower_bound:upper_bound]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=150))
plt.plot(x,fit_stocks[::-1])
plt.gcf().autofmt_xdate()
plt.plot(x,ydata[::-1],color='black')

plt.ylabel('S&P 500 value')
plt.xlabel('Date')