# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm

files = os.listdir("./19-04-26/")
files.sort()
#files=np.flip(files)

colors = cm.rainbow(np.linspace(0, 0.9, len(files)))

filtro_3=396.45
filtro_2=21.38
filtro_1=8.1

filtro=np.array([filtro_3, filtro_3*filtro_1,filtro_3*filtro_2*filtro_1 ])/(filtro_3*filtro_2*filtro_1)
#filtro=np.flip(filtro)

counter=0
x,y = np.loadtxt("potencia.txt", unpack=True)
print(y)

#Offset curvas según gnuplot
a= 877.541 

#inicial
filtro_total=filtro[0]
offset_plot=0

#mpl. params es para cambiar el tamaño de la letra y hacer el fucking autolayout. READ THE DOCSs#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 24,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################

def style(number):
	plt.figure(number)
	plt.ylabel("Intensidad [u.a.]")
	plt.xlabel(u"Energía [eV]")
	plt.xlim(1.5307,1.5338)
	plt.grid(alpha=0.4)

style(1) #Primer plot
for file in files:
	x,y_ = np.loadtxt("./19-04-26/"+file,unpack=True)

	if counter==25:
		style(2) #Segundo plot
		filtro_total=filtro[1]

	elif counter==29:
		filtro_total=filtro[2]


	plt.plot(1239.8/x, offset_plot+ filtro_total*(y_-a), color=colors[counter-18], label=str(y[counter])+" mW")

	counter+= 1 
	offset_plot+=2 if counter <=25 else 10
	plt.yscale('log')
	plt.legend(loc='upper center', ncol=1)

#cositos
mpl.rcParams.update({'font.size': 24,  'figure.figsize': [18, 8],  'figure.autolayout': True})

#files_fit=["L0_26_Abril.txt", "L1_26_Abril.txt", "L2_26_Abril.txt"]
#label_fit=["L0 Condensa","L1 Condensa despues","L2 No condensa"]
x,y = np.loadtxt("potencia.txt", unpack=True)

files_fit=["L1_26_Abril.txt", "L2_26_Abril.txt"]
label_fit=["L1","L2"]

yones=np.ones(len(y))

pdi="PDI"

fig=plt.figure(3)
for x in range(len(files_fit)):
	centro, err_centro, fwhm, fwhm_err, Area, Area_Err = np.loadtxt(files_fit[x], unpack=True)

	#y=y[:1 if type(centro)==np.float64 else len(centro)]

	ax1 = fig.add_subplot(12*10+x+1)
	ax1.set_title(label_fit[x])
	area = ax1.plot(y,fwhm*1000.0, linestyle='--',  marker='^', ms= 8 , c='r')
	ax1.set_xscale('log')
	ax1.tick_params(axis='y', colors='red')
	ax1.plot(y, yones*0.025, c='b', linestyle='-', label="LPO")
	ax1.plot(y, yones*0.06, c='r', linestyle='--', label=pdi)
	ax1.legend(loc='center left', ncol=1)
	

	ax2 = fig.add_subplot(12*10+x+1, sharex=ax1, frameon=False)
	wide = ax2.plot(y,Area,  ':', markersize= 8 , marker='s', color='black')
	#ax2.yaxis.label.set_color('red')
	ax2.set_yscale('log')
	ax2.yaxis.tick_right()
	ax2.yaxis.set_label_position("right")


	if x==0: 
		ax1.set_ylabel(u"FWHM [meV] \u25B4 ")
		ax1.yaxis.label.set_color('red')
		ax1.tick_params(axis='y', colors='red')
		ax1.set_xlabel(u"Potencia [mW]")

	if x==1:
		ax2.set_ylabel(u"Intensidad [u.a] \u25A0")
		ax2.yaxis.label.set_color('black')
		ax2.set_xlabel("Potencia [mW]")

plt.show()
