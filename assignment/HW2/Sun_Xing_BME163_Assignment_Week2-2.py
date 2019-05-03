import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import time
import math
plt.style.use('BME163.mplstyle')

file = open("BME163_Input_Data_1.txt","r")
x_values = []
y_values = []

for row in file:

    data = row.split()
    x_values += [data[1]]
    y_values += [data[2]]

x = x_values[:-5]
y = y_values[:-5]


for i in range(len(x_values)):
    x_values[i] = math.log2(int(x_values[i])+1)
for i in range(len(y_values)):
    y_values[i] = math.log2(int(y_values[i])+1)


figure_width=5
figure_height=2

plt.figure(figsize=(figure_width,figure_height))

panel_width=1/figure_width
panel_height=1/figure_height
panel2_width = 0.25/figure_width
panel2_height = 1/figure_height
panel3_width = 1/figure_width
panel3_height = 0.25/figure_height

panel1=plt.axes([0.14,0.15,panel_width,panel_height])
panel2=plt.axes([0.075,0.15,panel2_width,panel2_height])
panel3=plt.axes([0.14,0.683,panel3_width,panel3_height])


panel1.tick_params(axis='both',which='both',
                   bottom='on', labelbottom='on',
                   left='off', labelleft='off',
                   right='off', labelright='off',
                   top='off', labeltop='off')
# panel2.tick_params(axis='both',which='both',
#                    bottom='on', labelbottom='on',
#                    left='off', labelleft='off',
#                    right='off', labelright='off',
#                    top='off', labeltop='off')
panel3.tick_params(axis='both',which='both',
                   bottom='off', labelbottom='off',
                   left='on', labelleft='on',
                   right='off', labelright='off',
                   top='off', labeltop='off')
panel1.set_xlim(0,15)
panel1.set_ylim(0,15)
panel2.set_xlim(20,0)
panel2.set_ylim(0,15)

# panel3.set_xlim(0,15)
# panel3.set_ylim(0,20)

panel1.plot(x_values,y_values,
             color='black',
             marker='o',
             markeredgecolor='red',
             markeredgewidth=0,
             markerfacecolor='black',
             markersize=1.4,
             linewidth=0,
             linestyle='--',
             alpha=0.1)


bins = np.linspace(0,15,31)

# print(bins,len(bins))

x_histo, bins=np.histogram(x_values,bins)
# print(x_histo)
# print(len(x_histo),len(bins))

for index in range(0,len(x_histo),1):
    bottom=0
    left=bins[index]
    width=bins[index+1]-left
    height=math.log2(x_histo[index]+1)
    rectangle1=mplpatches.Rectangle([left,bottom],width,height,
                                edgecolor='black',
                                facecolor='grey',
                                linewidth=0.1,
                                )
    panel3.add_patch(rectangle1)
panel3.set_xlim(0,15)
panel3.set_ylim(0,20)

bins = np.linspace(0,15,31)

# print(bins,len(bins))

y_histo, bins=np.histogram(y_values,bins)
# print(y_histo)
# print(len(y_histo),len(bins))

for index in range(0,len(y_histo),1):
    bottom = bins[index]
    left= 0
    width=math.log2(y_histo[index]+1)
    height=bins[index+1]-bottom

    rectangle1=mplpatches.Rectangle([left,bottom],width,height,
                                edgecolor='black',
                                facecolor='grey',
                                linewidth=0.1,
                                )
    panel2.add_patch(rectangle1)


panel4=plt.axes([0.54,0.15,panel_width,panel_height])
panel5=plt.axes([0.476,0.15,panel2_width,panel2_height])
panel6=plt.axes([0.54,0.683,panel3_width,panel3_height])

panel4.tick_params(axis='both',which='both',
                   bottom='on', labelbottom='on',
                   left='off', labelleft='off',
                   right='off', labelright='off',
                   top='off', labeltop='off')
# panel2.tick_params(axis='both',which='both',
#                    bottom='on', labelbottom='on',
#                    left='off', labelleft='off',
#                    right='off', labelright='off',
#                    top='off', labeltop='off')
panel6.tick_params(axis='both',which='both',
                   bottom='off', labelbottom='off',
                   left='on', labelleft='on',
                   right='off', labelright='off',
                   top='off', labeltop='off')


panel5.set_xlim(20,0)
panel5.set_ylim(0,15)
panel6.set_xlim(0,15)
panel6.set_ylim(0,20)


for index in range(0,len(x_histo),1):
    bottom=0
    left=bins[index]
    width=bins[index+1]-left
    height=math.log2(x_histo[index]+1)
    rectangle1=mplpatches.Rectangle([left,bottom],width,height,
                                edgecolor='black',
                                facecolor='grey',
                                linewidth=0.1,
                                )
    panel6.add_patch(rectangle1)

for index in range(0,len(y_histo),1):
    bottom = bins[index]
    left= 0
    width=math.log2(y_histo[index]+1)
    height=bins[index+1]-bottom

    rectangle1=mplpatches.Rectangle([left,bottom],width,height,
                                edgecolor='black',
                                facecolor='grey',
                                linewidth=0.1,
                                )
    panel5.add_patch(rectangle1)






bins = (np.linspace(0,15,61),np.linspace(0,15,61))



bins, x_edges, y_edges=np.histogram2d(x_values, y_values, bins)


print(np.shape(bins))

maxi = np.max(bins)
print(maxi)
for i in range(0,60):
    for j in range(0,60):
        a = bins[i][j]/20 if bins[i][j] <=20 else 1
        rectangle1 = mplpatches.Rectangle([i/4,j/4],15/60,15/60,
                                          # edgecolor="black",
                                          facecolor=(1-a,1-a,1-a),
                                          linewidth = 0)
        panel4.add_patch(rectangle1)

panel4.set_xlim(0,15)
panel4.set_ylim(0,15)

panel7_width = 0.1/figure_width
panel7=plt.axes([0.8,0.15,panel7_width,panel_height],yticks = [0,10,20],yticklabels = ["0","10",">20"])
panel7.tick_params(axis='both',which='both',
                   bottom='off', labelbottom='off',
                   left='on', labelleft='on',
                   right='off', labelright='off',
                   top='off', labeltop='off')
panel7.set_xlim(0,1)
panel7.set_ylim(0,20)

for i in range(0,20):
    rectangle1 = mplpatches.Rectangle([0,i],1,1,
                                      facecolor = (1-i/19,1-i/19,1-i/19),
                                      linewidth=0)
    panel7.add_patch(rectangle1)


plt.savefig('Sun_Xing_BME163_Assignment_Week2.png',dpi=600)



