import os
import sys
import matplotlib as mpl

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns


#mpl.params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 30,  'figure.figsize': [10, 8],  'figure.autolayout': True})
#######################################################


directory= "./Nitrogeno/LT/"

files = os.listdir(directory)

for x in files:
	x=float(x)

files.sort()

index=0
colors = cm.rainbow(np.linspace(0, 0.9, len(files)))
offset=0.0
offset1=0.0

A=117

plt.figure(0)
x,y = np.loadtxt("./Nitrogeno/LT/32.95", unpack=True)
plt.plot(1239.8/x,(y-875)/A)
plt.ylabel("Intensidad [u. a.]")
plt.xlabel("Energía [eV]")
plt.xlim(1.516,1.547)


x1,y1,x2,y2=1.535 , 0.79 , 1.5229 , 0.79  
plt.annotate("", xy=(x1,y1),xytext=(x2,y2),arrowprops=dict(arrowstyle="<-") )
x1,y1=1.535 -0.0075, 0.79   
plt.text(x1, y1, "LP\n(Modo de Cavidad)" ,bbox= dict(boxstyle="round", fc="w", ec="k", pad=0.2) )

x1,y1,x2,y2= 1.52889, 0.2  , 1.52889 , 0.45 
plt.annotate("", xy=(x1,y1),xytext=(x2,y2),arrowprops=dict(arrowstyle="->") )
x2,y2= 1.52889 , 0.45
plt.text(x2, y2, "MP\n (HH)" ,bbox= dict(boxstyle="round", fc="w", ec="k", pad=0.2) )

x1,y1,x2,y2= 1.54138, 0.2, 1.54138 , 0.45
plt.annotate("", xy=(x1,y1),xytext=(x2,y2),arrowprops=dict(arrowstyle="->") )
x2,y2= 1.54138  , 0.45
plt.text(x2, y2, "UP\n (LH)" ,bbox= dict(boxstyle="round", fc="w", ec="k", pad=0.2) )

##cosas para el subplot
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)# at the lower left corner (loc=3)

fig, ax = plt.subplots()
ax2 = plt.axes([0,0,1,1])
ip=InsetPosition(ax, [0.38,0.4,0.6,0.55])
ax2.set_axes_locator(ip)
mark_inset(ax, ax2, loc1=1, loc2=2, fc="none", ec='0.5', alpha=0.0)
#############################

for filename in files:
	x,y =np.loadtxt(directory + filename, unpack=True)
	#print(x)
	ax.plot(1239.8/x,offset1+(y-800)/44000,label=str(files[index]), c=colors[index])
	im=ax2.plot(1239.8/x,offset1+(y-800)/44000,label=str(files[index]), c=colors[index])
	#sns.lmplot(data=zip(x,y))
	offset1+=0.0100
	index+=1
	pass
#plt.legend(loc='upper left', ncol=1)
ax.set_xlim(1.5119,1.5398)
ax.set_ylabel("Intensidad [u. a.]")
ax.set_xlabel("Energía [eV]")

#plt.legend(loc='upper left', ncol=1)
ax2.set_xlim(1.5120,1.5395)
ax2.set_ylim(0,0.41)
#ax2.set_ylabel("Intensidad [u. a.]")
#ax2.set_xlabel("Energía [eV]")
plt.show()
