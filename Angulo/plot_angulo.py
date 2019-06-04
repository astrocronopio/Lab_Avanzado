import os
import sys
import numpy as np

#mpl. params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 18,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################


directory= "./Angulo/"


files = ["4", "5.2", "9.5", "13.5", "19.3", "25", "54"]
angulos=[]

for x in files:
	x=float(x)

for x in files:
	angulos.append(180.0*np.arctan(float(x)/200.0)/(2.0*np.pi))
	pass

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# test data

index=0

colors = cm.rainbow(np.linspace(0, 1, len(files)))

plt.figure(0)
x,y=np.loadtxt("./Angulo/4", unpack=True)
plt.plot(1239.8/x,y/25400, label=str(float("{0:.2f}".format(angulos[0])))+"°", c=colors[0])
plt.legend(loc='upper left', ncol=1)
plt.xlabel("Energía [eV]")
plt.ylabel("Intensidad [u.a.]")
plt.grid(alpha=0.2)
plt.xlim(1.411,1.4165)
plt.ylim(0,1)



plt.figure(1)
for x in files:
	data=np.loadtxt(directory + str(x))
	print(x)
	index+=1
	x=data[:,0]
	y=data[:,1]
	plt.plot(1239.8/x,y/25400,label=str(float("{0:.2f}".format(angulos[index-1])))+"°", c=colors[index-1])
plt.legend(loc='upper left', ncol=1)
plt.xlabel("Energía [eV]")
plt.ylabel("Intensidad [u.a.]")
plt.grid(alpha=0.2)
plt.xlim(1.411,1.4165)
plt.ylim(0,1)
plt.show()


