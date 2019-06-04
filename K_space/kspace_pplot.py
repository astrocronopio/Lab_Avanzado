#encoding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import os

############3
#mpl. params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 30,  'figure.figsize': [10, 9],  'figure.autolayout': True})
#######################################################

filename = "./20190314_vuelta_sobre_la_muestra/matrices/k_space06_LT_15s_P=3.5mW.txt"
spectrum = "./20190314_vuelta_sobre_la_muestra/espectros/k_espectro06_LT_1s_P=3.5mW.txt"

#filename = "./20190314_vuelta_sobre_la_muestra/matrices/k_space02_LT_15s_P=6mW.txt"
#spectrum = "./20190314_vuelta_sobre_la_muestra/espectros/k_espectro02_LT_1s_P=6mW.txt"


pixel_x= np.loadtxt(filename, max_rows=1)

#os.system("sed -i '1d' " + filename) #Cuando no le borre todavia la cosa de arriba a la matriz

#the matrix plot
data=np.loadtxt(filename)
print(data)
pixel_y= data[:,0]
data=np.delete(data,0,1)
data=data.transpose()
data=np.log(data)
NA= 0.582364238 *180/np.pi

# the scatter plot:
x,y = np.loadtxt(spectrum, unpack=True)
max_= y.max()
y=y/max_

#print matrix
plt.figure(3)
data=np.log(data)
max_= data.max()
data=data/max_


plt.ylabel(u"Energía [eV]")
plt.xlabel("Angulo [$^o$]")

pixel_y=np.array([2*NA*(pixel-146)/128 for pixel in pixel_y ])

plt.pcolor(pixel_y,1239.8/x, data,cmap='jet')

cbar = plt.colorbar(shrink=0.7)#, ticks=[1.0, 0.95, 0.90,0.85])
cbar.set_label('Intensidad Norm. (log) [u.a.]')
#cbar.ax.set_yticklabels(['< -1', '0', '> 1']) 

plt.ylabel(u"Energía [eV]")
plt.xlabel("Angulo [$^o$]")

plt.show()
