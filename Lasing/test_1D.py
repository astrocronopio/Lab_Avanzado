# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np
from numpy import transpose
import matplotlib.gridspec as gridspec
import matplotlib as mpl
#from matplotlib.axes.Axes.tick_params 
#mpl.rcParams['savefig.pad_inches'] = 0
#plt.rcParams["figure.figsize"] = 7,5

#cositos
mpl.rcParams.update({'font.size': 30,  'figure.figsize': [14, 8],  'figure.autolayout': False})

fin = lambda x: x[-1]+(x[1]-x[0])/2.
inicio = lambda x : x[0]-(x[1]-x[0])/2.


filtro_3=396.45
filtro_2=21.38
filtro_1=8.1

filtro=np.array([filtro_3, filtro_3*filtro_1,filtro_3*filtro_2*filtro_1 ])/(filtro_3*filtro_2*filtro_1)
#filtro=np.flip(filtro)

counter=0
#Offset curvas según gnuplot
a= 877.541 

#inicial
filtro_total=filtro[0]


#y, potencia = np.loadtxt("C:\\Users\\HP2017\\Desktop\\Evelyn\\Condensacion\\potencia.txt", unpack=True)

y, potencia = np.loadtxt("potencia.txt", unpack=True)

def print_heatmap(file, ax, filtro_total):
	x0,y0= np.loadtxt(direc+file, unpack=True)
	x0=1239.8/x0
	y0=(-a+y0)*filtro_total

	y0=y0/y0.max()

	x0=np.flip(x0)
	y0=y0[np.newaxis,:]
	
	extent0 = [0,1,inicio(x0), fin(x0)]
	im=ax.imshow(y0.transpose(), cmap="jet", extent=extent0, aspect="auto")
	ax.set_xlim(extent0[0], extent0[1])
	ax.spines['left'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.tick_params(axis="y", size=0.0) 
	ax.set_xticks([])
	return im

#direc= "C:\\Users\\HP2017\\Desktop\\Evelyn\\Condensacion\\19-04-26\\"
direc= "./19-04-26/"
files=os.listdir(direc)
files.sort()
print(files)


fig, ax = plt.subplots(ncols=len(files), sharey=True)
plt.subplots_adjust(wspace=0.0, hspace=0, right=0.8, bottom=0.15, left=0.15)
plt.axes([0,0,1,1], frameon=False)

cbar_ax = fig.add_axes([0.85, 0.15, 0.025, 0.7])



for x in range(0,len(files)):
	if counter==25:
		filtro_total=filtro[1]

	elif counter==29:
		filtro_total=filtro[2]

	im=print_heatmap(files[x], ax[x], filtro_total)

	if x%5==0:
		ax[x].text(0.0,1.52615, "{:.1f}".format(potencia[x]/4))#, rotation='vertical') 
	counter+=1

#ax[0].set_ylabel(u"Energía [eV]")
ax[0].set_ylabel(u"Energy [eV]")

ax[0].spines['left'].set_visible(True)
ax[0].tick_params(axis="y", size=5) 
ax[-1].spines['right'].set_visible(True)
ax[-1].yaxis.tick_right()
ax[-1].tick_params(axis="y", size=5) 

fig.text(0.71,0.8, "L2", {'color': 'white', 'fontsize': 30, 'ha': 'center', 'va': 'center'})
fig.text(0.71,0.6, "L1", {'color': 'white', 'fontsize': 30, 'ha': 'center', 'va': 'center'})
#, rotation='vertical')


# the arrow
"""

ax.annotate("", xy=(-0.174, 0.762), xycoords='data',
             xytext=(-0.174, 0.550), textcoords='data',
             arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
plt.text(0.174,0.5*(0.761857 + 0.549950), r'1.85 meV',
         {'color': 'k', 'fontsize': 24, 'ha': 'center', 'va': 'center',
          'bbox': dict(boxstyle="round", fc="w", ec="k", pad=0.2)})


plt.annotate("", xy=(0.174,  0.550), xycoords='data',
             xytext=(0.174,0.342), textcoords='data',
             arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))
plt.text(0.174,0.5*(0.550 + 0.342), r'2.06 meV',
         {'color': 'k', 'fontsize': 24, 'ha': 'center', 'va': 'center',
          'bbox': dict(boxstyle="round", fc="w", ec="k", pad=0.2)})

"""

#fig.text(0.42,0.018, "Potencia [mW]")#, rotation='vertical')
fig.text(0.42,0.018, "Power [mW]")#, rotation='vertical')
fig.text(0.32,0.81, "3.2x3.2 $\mu$m", {'color': 'k', 'fontsize': 30, 'ha': 'center', 'va': 'center',
          'bbox': dict(boxstyle="round", fc="w", ec="k", pad=0.2)})#, rotation='vertical')

cbar=fig.colorbar(im, cax=cbar_ax,shrink=0.2)

#cbar.set_label('Intensidad (log) [u.a.]')
cbar.set_label('PL Intensity Norm. [a.u.]')

plt.show()
