import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#mpl.params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 30,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################

#Acá estás los archivos que queres plotear
directory= "./Nitrogeno/LT/"

files = os.listdir(directory)

#Los archivo están ordenados por el nombre
files.sort()

#Para el color
colors = cm.rainbow(np.linspace(0, 0.9, len(files)))

index=0
offset1=0.0

##cosas para el subplot
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)# left corner (loc=3)

fig, ax = plt.subplots()
ax2 = plt.axes([0,0,1,1])
ip=InsetPosition(ax, [0.38,0.4,0.6,0.55])
ax2.set_axes_locator(ip)
mark_inset(ax, ax2, loc1=1, loc2=2, fc="none", ec='0.5', alpha=0.0)
#############################

for filename in files:
	x,y =np.loadtxt(directory + filename, unpack=True)
	
	ax.plot( 1239.8/x, offset1+(y-870)/44000, c=colors[index])
	ax2.plot(1239.8/x, offset1+(y-870)/44000, c=colors[index])

	offset1+=0.0100
	index+=1
	pass
#plt.legend(loc='upper left', ncol=1)
ax.set_xlim(1.5119,1.5398)
ax.set_ylabel("Intensidad [u. a.]")
ax.set_xlabel("Energía [eV]")

##Cosas del inset
ax2.set_xlim(1.5120,1.5395)
ax2.set_ylim(0,0.41)
#ax2.set_ylabel("Intensidad [u. a.]")
#ax2.set_xlabel("Energía [eV]")
plt.show()