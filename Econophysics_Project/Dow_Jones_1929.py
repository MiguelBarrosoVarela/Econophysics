# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 18:19:15 2022

@author: Hugo Rauch
"""
"""https://fred.stlouisfed.org/series/M1109BUSM293NNBR"""

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit
from matplotlib.widgets import Slider, Button


stock_values=np.loadtxt('DJIA.csv',skiprows=1,usecols=1,delimiter=',')
dates=np.linspace(0,len(stock_values)-1,len(stock_values),dtype=float)



"""Trying to load dates"""
true_dates=np.loadtxt('DJIA.csv',skiprows=1,usecols=0,delimiter=',',dtype=str)

#Removing days where stock_values=0
closed_market_dates=[]
for date in range(len(stock_values)):
    if stock_values[date]==0:
        closed_market_dates.append(date)
stock_values=np.delete(stock_values,closed_market_dates)
true_dates=np.delete(true_dates,closed_market_dates)




#Flipping stock values (in original data set recent values at top)
stock_values=stock_values[::-1]   

fit_times=dates[14606:14800]
fit_prices=stock_values[14606:14800]
plt.plot(fit_times,fit_prices)


def LogPeriodic(t,tc,a,w,C,A,B,P):
    return A+(B*(tc-t)**a)*(1 + C*np.cos(w*np.log(tc-t) + P))


plot_y=LogPeriodic(fit_times,*p0)
plt.plot(fit_times,plot_y)
popt, pcov = curve_fit(LogPeriodic,fit_times,fit_prices, p0, maxfev=5000)


#%%%


# t goes to fit_times
# f goes to LogPeriodic


# Define initial parameters
tc=14810
init_w=11
init_C=0.2
init_B=2000
P=0
init_a=-0.5
A=-LogPeriodic(14606,tc,init_a,init_w,init_C,0,init_B,P)+1980


p0_init=[tc,init_a,init_w,init_C,A,init_B,P]

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = plt.plot(fit_times, LogPeriodic(fit_times, *p0_init), lw=2)
ax.set_xlabel('Time [s]')

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the w.
axw = plt.axes([0.25, 0.1, 0.65, 0.03])
w_slider = Slider(
    ax=axw,
    label='w',
    valmin=0,
    valmax=100,
    valinit=init_w,
)

# Make a vertically oriented slider to control the B
axB = plt.axes([0.05, 0.25, 0.0225, 0.63])
B_slider = Slider(
    ax=axB,
    label="B",
    valmin=0,
    valmax=50000,
    valinit=init_B,
    orientation="vertical"
)

# Make a vertically oriented slider to control the amplitude
axa = plt.axes([0.1, 0.25, 0.0225, 0.63])
a_slider = Slider(
    ax=axa,
    label="a",
    valmin=-10,
    valmax=0,
    valinit=init_a,
    orientation="vertical"
)


# Make a horizontal slider to control the C.
axC = plt.axes([0.25, 0.05, 0.65, 0.03])
C_slider = Slider(
    ax=axC,
    label='C',
    valmin=0,
    valmax=20,
    valinit=init_C,
)

# The function to be called anytime a slider's value changes
def update(val):
    A=-LogPeriodic(14606,tc,a_slider.val,w_slider.val,C_slider.val,0,B_slider.val,P)+2200
    line.set_ydata(LogPeriodic(fit_times,tc,a_slider.val,w_slider.val,C_slider.val,A,B_slider.val,P))
    fig.canvas.draw_idle()
    p0=[tc,a_slider.val,w_slider.val,C_slider.val,A,B_slider.val,P]
    popt, pcov = curve_fit(LogPeriodic,fit_times,fit_prices, p0, maxfev=5000)



# register the update function with each slider
B_slider.on_changed(update)
w_slider.on_changed(update)
a_slider.on_changed(update)
C_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = plt.axes([0.05, 0.15, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    B_slider.reset()
    w_slider.reset()
    a_slider.reset()
    C_slider.reset()

button.on_clicked(reset)

#plotting data
ax.plot(fit_times,fit_prices)




#%%

x = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in true_dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5000))
plt.plot(x,stock_values)
plt.gcf().autofmt_xdate()

"""
plt.plot(
    type="candle", 
    mav =(3,6,9),
    style="yahoo"
    )
"""