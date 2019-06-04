#encoding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import os
#mpl. params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 30,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################

filename = "./xspace/49_xs_.txt"
spectrum = "./espectro/49.txt"

pixel_x= np.loadtxt(filename, max_rows=1)

#os.system("sed -i '1d' " + filename) #Cuando no le borre todavia la cosa de arriba a la matriz

#the matrix plot
data=np.loadtxt(filename)
pixel_y= data[:,0]
data=np.delete(data,0,1)
data=data.transpose()
data=np.log(data)

# the scatter plot:
x,y = np.loadtxt(spectrum, unpack=True)
max_= y.max()
y=y/max_

#print matrix
plt.figure(3)
data=np.log(data)
#max_= data.max()
#data=data/max_

NA=2*1.6/8

plt.title("1.6x1.6 $\mu$m, 13 mW ")

pixel_y=np.array([NA*(pixel-154) for pixel in pixel_y ])

plt.pcolor(pixel_y,1239.8/x, data,cmap='jet')

cbar = plt.colorbar(shrink=0.7)#, ticks=[1.9, 2.0, 2.1,2.2,2.3])
cbar.set_label('Intensidad (log) [u.a.]')
#cbar.set_label('PL Intensity (log) [a.u.]')

plt.ylabel(u"Energía [eV]")
#plt.ylabel(u"Energy [eV]")

plt.xlabel("x [$\mu$m]")

plt.show()