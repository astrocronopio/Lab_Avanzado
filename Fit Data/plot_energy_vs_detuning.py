# -*- coding: utf-8 -*-

import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)# at the lower left corner (loc=3)


#mpl. params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 24,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################

import matplotlib.pyplot as plt

##los archivos de donde saco los datos
upper_polariton= "./upper_polariton.txt"
low_polariton= "./low_polariton.txt"
medium_polariton= "./medium_polariton.txt"

files= [upper_polariton, medium_polariton, low_polariton] ##para manejarlos

##en el archivo siguiente está las estimaciones numericas
z, fit_low, fit_medium, fit_upper = np.loadtxt("./eigenvalues.txt", unpack=True) #z es la distancia sobre la muestra
fitted=[ fit_upper,fit_medium, fit_low]

######################Cosas de estilo
pointype=['s', 'd', '^']
dashtype=['--', ':', '-']
name_plot=['UP', 'MP', 'LP']
#name_plot_fit=['Ajuste MP', 'Ajuste UP', 'Ajuste LP']
#####################3

#####Lo que fiteo el Mathematica###
#Se propusieron modelos lineales para las energías de Heavy y Light Hole
#Energia Heavy Hole
hh=1.5217
slope_hh=0.000084311
#Energia Light Hole
lw=1.52734
slope_lw=0.000076553

#Modo de Cavidad Cuadrático
#C(x) =1.41743 x* 0.00605565 +0.000024793*x**2
A=1.41743
B=0.00608928
C=0.00002244

#Rabbi Splitting
Rabbi_lh= 0.00193*2.0 
Rabbi_hh= 0.00298*2.0
###################################3

z=A+z*B+C*z**2-(hh + slope_hh*z)
z=1000*z #para poner en mEv

index=0
colors = ['red', 'blue', 'black']


##cosas para el subplot
fig, ax = plt.subplots()
ax2 = plt.axes([0,0,1,1])
ip=InsetPosition(ax, [0.59,0.08,0.4,0.4])
ax2.set_axes_locator(ip)
mark_inset(ax, ax2, loc1=1, loc2=2, fc="none", ec='0.5')

fig_sin_fit, ax_sin_fit = plt.subplots()
ax_sin_fit_2  = plt.axes([0,0,1,1])
ip1=InsetPosition(ax_sin_fit , [0.59,0.08,0.4,0.4])
ax_sin_fit_2.set_axes_locator(ip1)
mark_inset(ax_sin_fit , ax_sin_fit_2, loc1=1, loc2=2, fc="none", ec='0.5')
#############################

for filename in files:
	data=np.loadtxt(filename)
	x=data[:,0]

	heavy= hh + slope_hh*x
	light= lw + slope_lw*x
	cavity_mode = A+x*B+C*x**2

	x=A+x*B+C*x**2-(heavy)

	x=1000*x #para poner en mEv
	
	wavelength=data[:,1]
	wavelength_err=data[:,2]

	fhwm=data[:,3]
	fhwm_err=data[:,4]

	fhwm=fhwm*1239.8/wavelength**2
	fhwm_err=fhwm_err*1239.8/wavelength**2

	area=data[:,5]
	area_err= data[:,6]

	y= np.ones(len(x))


	plt.figure(1)

	##La figura más importante de esta parte, los modos de cavidad
	ax.plot(x, cavity_mode, '--', alpha=0.4)
	ax.plot(x,heavy, '--', alpha=0.4)
	ax.plot(x,light, '--', alpha=0.4)

	ax.plot(x, 1239.8/wavelength, pointype[index], markersize=8, c=colors[index], label=name_plot[index])
	
	#Con z porque no tiene la misma dimension con x
	if index!=2:
		ax.plot(z, fitted[index], c="black")
	else:
		ax.plot(z, fitted[index], c="black", label="Ajuste")

	ax.text(-80,1.54, "$\Omega_{HH}=5.96\,$meV\n$\Omega_{LH}=3.86\,$meV", bbox=dict(facecolor='white', alpha=0.5))

	
	##El inset de la foto
	ax2.plot(x, cavity_mode, '--', alpha=0.4)
	ax2.plot(x,heavy, '--', alpha=0.4)
	ax2.plot(x,light, '--', alpha=0.4)
	ax2.plot(x, 1239.8/wavelength, pointype[index], c=colors[index], label=name_plot[index],markersize=8)
	#Con z porque no tiene la misma dimension con x
	ax2.plot(z, fitted[index], c="black")#, label=name_plot_fit[index])
	ax2.grid(alpha=0.2)
	##Arrow HH
	x1,y1,x2,y2= 0.0, 1.5198 , 0.0, 1.5198 + Rabbi_hh
	ax2.annotate("", xy=(x1,y1),xytext=(x2,y2),arrowprops=dict(arrowstyle="<->") )
	ax2.text(x1+1, (y1+y2)*0.5, "$\Omega_{HH}$" ,bbox= dict(boxstyle="round", fc="w", ec="k", pad=0.2) )

	##Arrow LH
	x1,y1,x2,y2= 5.5, 1.5275 , 5.5, 1.5275 + Rabbi_lh
	ax2.annotate("", xy=(x1,y1),xytext=(x2,y2),arrowprops=dict(arrowstyle="<->") )
	ax2.text(x1+1, (y1+y2)*0.5, "$\Omega_{LH}$" ,bbox= dict(boxstyle="round", fc="w", ec="k", pad=0.2) )


	ax.errorbar(x, 1239.8/wavelength, c=colors[index], yerr= 1239.8*wavelength_err/(wavelength*wavelength), fmt=pointype[index])
	ax.legend(loc='center left', ncol=1, handler_map={})
	ax.set_ylabel("Energía [eV]")
	ax.set_xlabel(" $\delta$ [meV]")
	ax.grid(alpha=0.3)



	##################La figura del área de cada pico#######33
	plt.figure(5)
	plt.ylabel("Área [u.a.]")
	plt.xlabel(" $\delta$ [meV]")
	plt.plot(x, area,  pointype[index], c=colors[index], label=name_plot[index] )
	plt.legend(loc='upper left',handler_map={})#, loc='upper left', ncol=1)
	plt.errorbar(x, area, yerr=area_err, c=colors[index])
	plt.grid(alpha=0.2)
	plt.xlim(-20,20)

	##################La figura de el ancho de cada pico#######33
	plt.figure(3) 
	plt.ylabel("FHWM [meV]")
	plt.xlabel(" $\delta$ [meV]")
	plt.grid(alpha=0.2)
	plt.plot(x, 1000*fhwm,  pointype[index],c=colors[index], label=name_plot[index] )
	plt.errorbar(x, 1000*fhwm, yerr=fhwm_err, c=colors[index])
	plt.legend(loc='upper left',handler_map={})
	
	plt.figure(4) 
	plt.ylabel("FHWM$^{-1}$ [meV$^{-1}$]")
	plt.xlabel(" $\delta$ [meV]")
	plt.grid(alpha=0.2)
	plt.plot(x, 1/fhwm,  pointype[index],c=colors[index], label=name_plot[index] )
	plt.errorbar(x, 1/fhwm, yerr=fhwm_err/(fhwm*fhwm), c=colors[index])
	plt.legend(loc='center left',handler_map={})
	plt.xlim(-20,20)

	index+=1


###Sin el fiteo
plt.figure(2)
ax_sin_fit.grid(alpha=0.3)
ax_sin_fit.plot(x, cavity_mode, '--', label="Modo de Cavidad")
ax_sin_fit.plot(x,heavy, '--', label="HH")
ax_sin_fit.plot(x,light, '--', label="LH")
ax_sin_fit.legend(loc='center left',handler_map={})
ax_sin_fit.set_ylabel("Energía [eV]")
ax_sin_fit.set_xlabel(" $\delta$ [meV]")
##El inset de la foto
ax_sin_fit_2.plot(x, cavity_mode, '--')
ax_sin_fit_2.plot(x,heavy, '--')
ax_sin_fit_2.plot(x,light, '--')
ax_sin_fit_2.grid(alpha=0.4)

ax2.set_xlim(-3,12)
ax2.set_ylim(1.518,1.535)
ax_sin_fit_2.set_xlim(-3,12)
ax_sin_fit_2.set_ylim(1.518,1.535)
#ax2.set_ylabel("Energía [eV]")
#ax2.set_xlabel(" $\delta$ [meV]")

plt.show()
