import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import string 

filename0 ="./20190314_vuelta_sobre_la_muestra/matrices/k_space07_LT_15s_P=3.5mW.txt"
filename1="./20190314_vuelta_sobre_la_muestra/matrices/k_space05_LT_15s_P=3.5mW.txt"
filename2="./20190314_vuelta_sobre_la_muestra/matrices/k_space01_LT_5s_P=6mW.txt"

files=[filename0, filename1, filename2]

#upper_limit=3000
#lower_limit=1000
up0=40940
lo0=8000

up1= 5000
lo1= 900

up2= 5000
lo2= 900

up=[up0, up1, up2]
lo=[lo0, lo1, lo2]

espectrum0 ="./20190314_vuelta_sobre_la_muestra/espectros/k_espectro07_LT_1s_P=3.5mW.txt"
espectrum1="./20190314_vuelta_sobre_la_muestra/espectros/k_espectro05_LT_1s_P=3.5mW.txt"
espectrum2="./20190314_vuelta_sobre_la_muestra/espectros/k_espectro01_LT_1s_P=6mW.txt"

espectro=[espectrum0, espectrum1, espectrum2]

def extract_points(array, upper_limit,lower_limit , pixel_y, output):
	x=[]
	y=[]
	for pixel_x in range(len(array)):
		if array[pixel_x]< upper_limit and  array[pixel_x]> lower_limit:
			x.append(pixel_x)
			y.append(pixel_y)
			output.write("%f \t %f \n" %(float(pixel_x),float(pixel_y)))
			pass
		pass
	return np.array(x),np.array(y)

cual=1

#espectrum=espectro[cual]
#filename=files[cual]
#upper_limit=up[cual]
#lower_limit=lo[cual]

matrices=np.zeros((256,1024))

espectrum=espectro[cual]
filename=files[cual]	
upper_limit=up[cual]
lower_limit=lo[cual]

file_of_points= open(filename.replace('matrices','text_files'), "w+")

#El archivo del espectro
plt.figure(0)
n,m=np.loadtxt(espectrum, unpack=True)
plt.plot(1239.8/n,m)

#para sacar parabola
plt.figure(1)
data=np.loadtxt(filename)
pixel_y= data[:,0]
data=np.delete(data,0,1)
x,y =[],[]
for index in range(len(pixel_y)):
	a,b =extract_points(data[index],upper_limit, lower_limit, pixel_y[index],file_of_points)
	plt.scatter(a,b, color='black', s=0.1)
	pass

#print matrix
plt.figure(3)
data=np.log(data)
#data[data<6.8]=0

data=data.transpose()
max_= data.max()
data=data/max_
plt.imshow(data, cmap='jet', aspect='auto') #, origin='lower', vmin=900, vmax=10000)
plt.colorbar()
plt.show()

