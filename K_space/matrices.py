from numpy import linalg as LA
import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#files=os.listdir("./matrices/")
files=["./20190314_vuelta_sobre_la_muestra/matrices/k_space07_LT_15s_P=3.5mW.txt"]
from matplotlib.colors import ListedColormap

cmap = ListedColormap(['k', 'w', 'r'])
print(files)

matrices=np.zeros((1024,256))

index=0

for filename in files:
	plt.figure(index)
	data=np.loadtxt(filename)
	pixel_x= np.arange(1023)+1.5
	
	#pixel_y= np.arange(255)+1.5
	pixel_y= data[:,0]
	data=np.delete(data,0,1)
	data=data.transpose()
	matrices+=data
	data=np.log(data)
	#data[data>100]=0

	#data[data>6.8]=1
	
	data[data<6.8]=0

	print(data)
	
	plt.matshow(data, cmap=cmap)
	index+=1

plt.figure(20)
plt.imshow(matrices)
#plt.imshow(np.log(matrices), cmap=cmap)

plt.show()

