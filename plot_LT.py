# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
import matplotlib as mpl

#cositos
mpl.rcParams.update({'font.size': 24,  'figure.figsize': [18, 8],  'figure.autolayout': True})

files_fit=[ "L1_LT.txt", "L2_LT.txt"]
label_fit=[ "L1_LT", "L2_LT"]




fig=plt.figure(3)
for x in range(len(files_fit)):
	centro, err_centro, fwhm, fwhm_err, Area, Area_Err = np.loadtxt(files_fit[x], unpack=True)

	ax1 = fig.add_subplot(12*10+x+1)
	ax1.set_title(label_fit[x])
	area = ax1.plot(centro,fwhm*1000,  '--', markersize= 8 , marker='^', color='red')
	#ax1.set_xscale('log')
	ax1.tick_params(axis='y', colors='red')

	ax2 = fig.add_subplot(12*10+x+1, sharex=ax1, frameon=False)
	wide = ax2.plot(centro,Area,  ':', markersize= 8 , marker='s', color='black')
	#ax2.yaxis.label.set_color('red')
	#ax2.set_yscale('log')
	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")

	if x==0: 
		ax1.set_ylabel("FWHM [meV] △ ")
		ax1.yaxis.label.set_color('red')
		ax1.tick_params(axis='y', colors='red')
		ax1.set_xlabel("Potencia [mW]")

	if x==1:
		ax2.set_ylabel("Intensidad [u.a] □ ")
		ax2.yaxis.label.set_color('black')
		ax2.set_xlabel("Potencia [mW]")

plt.show()