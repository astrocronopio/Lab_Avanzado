#encoding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import os

############3
#mpl. params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 30,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################

filename = "./M01_xspace.txt"
spectrum = "./M01_espectro_7-7mW.txt"

pixel_x= np.loadtxt(filename, max_rows=1)

#os.system("sed -i '1d' " + filename) #Cuando no le borre todavia la cosa de arriba a la matriz

#the matrix plot
data=np.loadtxt(filename)
pixel_y= data[:,0]
data=np.delete(data,0,1)
data=data.transpose()
data=np.log(data)
data=data/np.max(data)
# the scatter plot:
x,y = np.loadtxt(spectrum, unpack=True)
max_= y.max()
y=y/max_

#print matrix
plt.figure(3)
#data=np.log(data)
#max_= data.max()
#data=data/max_

NA=2*1.6/7

plt.title("3.2x3.2$\mu$m, 3.67 mW ")

#pixel_y=np.array([NA*(pixel-158) for pixel in pixel_y ])

plt.pcolor(pixel_y,1239.8/x, data,cmap='jet')
#plt.pcolor(pixel_y,x, data,cmap='jet')

cbar = plt.colorbar(shrink=0.7)#, ticks=[1.9, 2.0, 2.1,2.2,2.3])
cbar.set_label('Intensidad Norm. (log) [u.a.]')
#cbar.set_label('Norm. PL Intensity (log) [a.u.]')

plt.ylabel(u"Energía [eV]")
#plt.ylabel(u"Energy [eV]")

plt.xlabel("x [$\mu$m]")

plt.show()
