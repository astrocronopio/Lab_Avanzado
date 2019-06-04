# -*- coding: utf-8 -*-

import numpy as np

#mpl. params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 30,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

##los archivos de donde saco los datos
upper_polariton	= "./eigenvectors_UP.txt"
low_polariton	= "./eigenvectors_LP.txt"
medium_polariton= "./eigenvectors_MP.txt"

files= [upper_polariton, medium_polariton, low_polariton] ##para manejarlos

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

#index=0
colors = ['red', 'blue', 'black']

# definitions for the axes
left, width 	= 0.1, 0.28
bottom, height 	= 0.2, 0.70

rect_LP 	 = [left, bottom, width, height]
rect_MP 	 = [left +0.30, bottom, width, height] #[left, bottom_h, width, 0.3]
rect_UP 	 = [left +0.60, bottom, width, height] #[left_h, bottom, 0.3, height]

# start with a rectangular Figure
plt.figure(1, figsize=(18, 8))

axLP = plt.axes(rect_LP)
axMP = plt.axes(rect_MP)
axUP = plt.axes(rect_UP)


fg=[axUP, axMP, axLP]

nullfmt = NullFormatter()         # no labels

axMP.yaxis.set_major_formatter(nullfmt)
axUP.yaxis.set_major_formatter(nullfmt)

index_trucho=[2,1,0]


for index in index_trucho:
	filename=files[index]
	fif= fg[index] #plt.figure(index)
	x,eig1, eig2, eig3 = np.loadtxt(filename, unpack=True)

	heavy= hh + slope_hh*x
	light= lw + slope_lw*x
	cavity_mode = A+x*B+C*x**2
 
	x=A+x*B+C*x**2-(heavy)
	x=1000*x #para poner en mEv
	fif.set_title(name_plot[index])
	fif.plot(x,eig2, dashtype[1], lw=5 ,color=colors[1], label= "$\\|\\alpha\\|^2\\,$Cav")
	fif.plot(x,eig1, dashtype[0], lw=5 ,color=colors[0], label= "$\\|\\beta\\|^2\\,$HH")
	fif.plot(x,eig3, dashtype[2], lw=5 ,color=colors[2], label= "$\\|\\gamma\\|^2\\,LH$")

	fif.set_xlim(-40,20)
	fif.set_xticks([-35,-15,0,15])
	#fif.set_ylabel("Peso")

	fif.grid(alpha=0.4)
	index+=1

axMP.set_xlabel(" $\delta$ [meV]")
axLP.set_ylabel("Peso")
axUP.legend(loc='center left',handler_map={})	
plt.show()
