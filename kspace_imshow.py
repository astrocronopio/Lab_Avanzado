import numpy as np
import matplotlib.pyplot as plt
import os

############3


filename = "./K_space/20190314_vuelta_sobre_la_muestra/matrices/k_space06_LT_15s_P=3.5mW.txt"
spectrum = "./K_space/20190314_vuelta_sobre_la_muestra/espectros/k_espectro06_LT_1s_P=3.5mW.txt"

pixel_x= np.loadtxt(filename, max_rows=1)

#os.system("sed -i '1d' " + filename) #Cuando no le borre todavia la cosa de arriba a la matriz

#the matrix plot
data=np.loadtxt(filename)
pixel_y= data[:,0]
data=np.delete(data,0,1)
data=data.transpose()
data=np.log(data)
NA= 0.582364238 *180/np.pi

# the scatter plot:
x,y = np.loadtxt(spectrum, unpack=True)
max_= y.max()
y=y/max_
#plt.show()
"""
def lineal_angulo(x, x_0,E_0):
	NA= 0.582364238 
	c= 299792458
	h= 4.13E-15


	m= 2*NA/(103)

	return E_0*np.tan(m*(x-x_0))/(c*h)

from matplotlib.ticker import NullFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

nullfmt = NullFormatter()\tab \tab  # no labels

# definitions for the axes
left, width = 0.1, 0.62
bottom, height = 0.1, 0.75
bottom_h = left_h = left + width + 0.03

rect_scatter = [left, bottom, width, height]
rect_histy = [left_h, bottom, 0.2, height]

plt.figure(1, figsize=(8, 8))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

# no labels
axHisty.yaxis.set_major_formatter(nullfmt)

# the scatter plot:
x,y = np.loadtxt(spectrum, unpack=True)
max_= y.max()
y=y/max_

axHisty.plot(y, x)
axHisty.set_ylim(x[0], x[-1])
axHisty.invert_yaxis()

divider = make_axes_locatable(axScatter)
cax = divider.append_axes('left', size='5%', pad=1.0)

kspace=axScatter.imshow(data, interpolation='bilinear', cmap='jet', aspect='auto', extent= [-146,110, x[-1], x[0]])
plt.colorbar(kspace,  cax=cax, orientation='vertical')

"""
#print matrix
plt.figure(3)
data=np.log(data)
#max_= data.max()
#data=data/max_

pixel_y=np.array([2*NA*(pixel-146)/128 for pixel in pixel_y ])

plt.pcolor(pixel_y,1239.8/x, data,cmap='jet')#, aspect='auto')#, extent= [-146,110, x[-1], x[0]], yscale='inverse')#extent= [-2*NA*(146)/128,2*NA*(110)/128, x[-1], x[0]])
plt.colorbar()

plt.show()