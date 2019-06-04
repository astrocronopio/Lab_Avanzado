# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np
from numpy import transpose
import matplotlib.gridspec as gridspec
import matplotlib as mpl
#from matplotlib.axes.Axes.tick_params 
#mpl.rcParams['savefig.pad_inches'] = 0
plt.rcParams["figure.figsize"] = 7,5

fin = lambda x: x[-1]+(x[1]-x[0])/2.
inicio = lambda x : x[0]-(x[1]-x[0])/2.

#y, potencia = np.loadtxt("C:\\Users\\HP2017\\Desktop\\Evelyn\\Condensacion\\potencia.txt", unpack=True)

y, potencia = np.loadtxt("potencia.txt", unpack=True)


def print_heatmap(file, ax):
	x0,y0= np.loadtxt(direc+file, unpack=True)
	x0=1239.8/x0
	y0=np.flip(y0[np.newaxis,:], 1)
	extent0 = [0,1,inicio(x0), fin(x0)]
	ax.imshow(y0.transpose(), cmap="jet", extent=extent0)
	ax.set_xlim(extent0[0], extent0[1])
	ax.spines['left'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.tick_params(axis="y", size=0.0) 
	ax.set_xticks([])

#direc= "C:\\Users\\HP2017\\Desktop\\Evelyn\\Condensacion\\19-04-26\\"
direc= "./19-04-26/"
files=os.listdir(direc)
print(files)

fig, ax = plt.subplots(ncols=len(files), sharey=True)
plt.subplots_adjust(wspace=0.0, hspace=0)
plt.axes([0,0,1,1], frameon=False)

for x in range(0,len(files)):
	print_heatmap(files[x], ax[x])
	if x%3==0:
		ax[x].text(0.5,1.5348, str(potencia[x]))#, rotation='vertical') 

ax[0].set_ylabel(u"Energía [eV]")
ax[0].spines['left'].set_visible(True)

plt.text(0.5,0.01, "Potencia")#, rotation='vertical')
plt.show()
