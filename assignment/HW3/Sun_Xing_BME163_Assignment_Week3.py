# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 10:45:20 2019

@author: admin
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import time
import math
plt.style.use('BME163.mplstyle')

figure_width=3
figure_height=3

plt.figure(figsize=(figure_width,figure_height))
panel_width=2/figure_width
panel_height=2/figure_height

panel1=plt.axes([0.15,0.15,panel_width,panel_height],xlabel="log$_2$(fold change)", ylabel="-log$_1$$_0$(p-value)")
#%%
x_values = []
y_values = []
label = []
file = open("BME163_Input_Data_2.txt","r")
def helper(string):
    if 'E' not in string:
        return -math.log10(float(string))
    else:
        num_power = string.split("E")
        num = float(num_power[0])
        power = float(num_power[1])
        return -(power)-math.log10(num)
print(helper('8.79E-86'))

for row in file:
#    print(row)
    data = row.split( )
    # print(data)
    label += [data[0]]
    if data[1] != "NA":
        x_values += [float(data[1])]
    else:
        x_values += [0]
    if data[2] != "NA":
        y_values += [helper(data[2])]
    else:
        y_values += [0]
# print(x_values)
# print(y_values)



n = len(x_values)

colors = []
for i in range(n):
    if y_values[i] >= 8 and 2**abs(x_values[i]) > 10:
        colors += [(1,0,0)]
    else:
        colors += [(0,0,0)]

panel1.scatter(x_values,y_values,
               s=2,
               linewidths=0,
               facecolor=colors,
               edgecolors=colors,
               alpha=1)


for i in range(n):
    if y_values[i]>=30 and 2**x_values[i]<=1/10:
        panel1.text(x_values[i]-0.5,y_values[i],label[i],va='center',ha='right',fontsize = 6)






panel1.set_xlim(-12,12)
panel1.set_ylim(0,60)






plt.savefig('Sun_Xing_BME163_Assignment_Week3.png',dpi=600)
