import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import math




plt.style.use('BME163.mplstyle')

figure_width=3.42
figure_height=2

plt.figure(figsize=(figure_width,figure_height))

panel_width=1/figure_width
panel_height=1/figure_height

panel1=plt.axes([0.1,0.2,panel_width,panel_height])
panel2=plt.axes([0.6,0.2,panel_width,panel_height])


y = [num for num in map(math.cos,np.linspace(0,math.pi/2,25))]
x = [num for num in map(math.sin,np.linspace(0,math.pi/2,25))]
print(x)

red=(1,0,0)
green=(0,1,0)
blue=(0,0,1)
yellow=(1,1,0)

R=np.linspace(blue[0],yellow[0],25)
G=np.linspace(blue[1],yellow[1],25)
B=np.linspace(blue[1],yellow[1],25)

for index in range(25):
    panel1.plot(x[index],y[index],
                color = (x[index],x[index],x[index]),
                markersize=1,
                marker="o")
panel1.tick_params(axis='both',which='both',\
                   bottom='off', labelbottom='off',\
                   left='off', labelleft='off', \
                   right='off', labelright='off',\
                   top='off', labeltop='off')


G=[np.linspace(0,1,10)]*10
R = np.transpose(G)


for i in range(0,10,1):
    for j in range(9,-1,-1):
        rectangle1 = mplpatches.Rectangle([i,j],1,1,
                                          edgecolor="black",
                                          facecolor=(R[i][j],G[i][j],1),
                                          linewidth = 1)
        panel2.add_patch(rectangle1)

panel2.set_xlim(0,10)
panel2.set_ylim(0,10)

panel2.tick_params(axis='both',which='both',\
                   bottom='off', labelbottom='off',\
                   left='off', labelleft='off', \
                   right='off', labelright='off',\
                   top='off', labeltop='off')

plt.savefig('Xing_Sun_HW1.png',dpi=600)
