import os
import sys
import numpy as np
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition, mark_inset)# at the lower left corner (loc=3)


directory= "./Nitrogeno/RT/"


files = os.listdir(directory)
angulos=[]

for x in files:
	x=float(x)

files.sort()
print(files)
	

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

index=0
colors = cm.rainbow(np.linspace(0, 1, len(files)))

fig, ax = plt.subplots()
ax2 = plt.axes([0,0,1,1])
ip=InsetPosition(ax, [0.05,0.4,0.5,0.5])
ax2.set_axes_locator(ip)
mark_inset(ax, ax2, loc1=2, loc2=4, fc="none", ec='0.5')


offset=0.0

for x in files:
	x, y =np.loadtxt(directory + str(x), unpack=True)
	print(x)
	index+=1

	ax.plot(1239.8/x,y+offset,label=str(float(files[index-1])), c=colors[index-1])
	ax2.plot(1239.8/x,y+offset/10,label=str(float(files[index-1])), c=colors[index-1])
	offset+=0

ax.legend(loc='upper right', ncol=4)
ax.set_xlabel("Energía (eV)")
ax.set_ylabel("Intensidad (Cuentas)")
ax.grid(alpha=0.2)
ax2.set_xlim(1.432,1.48)
ax2.set_ylim(800,1500)
#ax2.set_xticklabels(ax2.get_xticks(), backgroundcolor='w')
ax2.tick_params(axis='x', which='major', pad=8)
#plt.xlim(875.5,878.5)

plt.show()
