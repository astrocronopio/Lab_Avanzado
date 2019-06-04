import os
import sys
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#mpl. params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 18,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################


directory= sys.argv[1]

files = os.listdir(directory)

index=0
colors = cm.rainbow(np.linspace(0, 1, len(files)))
offset=0.0
offset1=0.0

for filename in files:
	x,y =np.loadtxt(directory + filename, unpack=True)
	#print(x)
	plt.plot(1239.8/x,y,label=str(files[index]), c=colors[index-1])
	offset1+=0.0100
	index+=1
	pass
#plt.legend(loc='upper left', ncol=1)
#plt.xlim(1.5119,1.5398)
plt.ylabel("Intensidad [u. a.]")
plt.xlabel("Energía [eV]")

plt.legend(loc='upper left', ncol=1)
#ax2.set_ylabel("Intensidad [u. a.]")
#ax2.set_xlabel("Energía [eV]")
plt.show()
