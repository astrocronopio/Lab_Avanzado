#coding=utf-8

import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

files=['./A', './B', './Cavidad']
files_LT=['./A_LT', './B_LT', './Cavidad_LT']


upper_polariton= open("./upper_polariton.txt", "w+")
low_polariton= open("./low_polariton.txt", "w+")
medium_polariton= open("./medium_polariton.txt", "w+")

file=[medium_polariton, upper_polariton,  low_polariton]

pointype=['--*', '-o', '--+']
name_plot=['MP', 'UP', 'LP']

index=0

for x in files_LT:
	data=np.loadtxt(x)

	x=-data[:,0] +23.8 +28
	
	wavelength=data[:,1]
	wavelength_err=data[:,2]

	fhwm=data[:,3]
	fhwm_err=data[:,4]

	area=data[:,5]/46682
	area_err= np.sqrt(2.0)*fhwm_err/46682

	for i in range(len(x)):
		d, wv, wv_err, f, f_err ,a, a_err = x[i], wavelength[i], wavelength_err[i], fhwm[i], fhwm_err[i] ,area[i], area_err[i]
		file[index].write("%f \t %f \t %f \t %f \t %f \t %f \t %f \n" %(d, wv, wv_err, f, f_err,a, a_err))
		pass

	index+=1

index=0

for x in files:
	data=np.loadtxt(x)

	x=28-data[:,0] 
	
	wavelength=data[:,1]
	wavelength_err=data[:,2]

	fhwm=data[:,3]
	fhwm_err=data[:,4]

	area=data[:,5]/(46682*2.0)
	area_err= np.sqrt(2.0)*fhwm_err*0.5/46682

	for i in range(len(x)):
		d, wv, wv_err, \
		f, f_err ,a, a_err \
		= x[i], wavelength[i], wavelength_err[i], \
		fhwm[i], fhwm_err[i], area[i], area_err[i]
		file[index].write("%f \t %f \t %f \t %f \t %f \t %f \t %f \n" %(d, wv, wv_err, f, f_err,a, a_err))
		pass

	index+=1

plt.show()
