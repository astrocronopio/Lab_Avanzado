# -*- coding: utf-8 -*-
"""Este script esta hecho para fitear un lorentziana o un Voigt, graficas el fit y data
ademas de mostrar los residuos, imprime un archivo por cada pico, y ese archivo van 
el centro, ancho, area y sus errores
para agregar mas curvas, falta poner mas files output y definir un pico más
EL SCRIPT BORRA LOS ARCHIVOS ANTERIORES!
"""
import numpy as np 
from lmfit.models import LorentzianModel, LinearModel,  VoigtModel , ConstantModel
from lmfit import minimize, Parameters 
import datetime
import sys
import matplotlib.pyplot as plt
import os
import subprocess
import matplotlib as mpl
mpl.rcParams.update({'font.size': 18,  'figure.figsize': [15, 8],  'figure.autolayout': True})

#printea al file donde estan los datos
def print_to_fit_log(filename,data_energy_item, out, curva):
	amplitude = out.params['L'+str(curva)+'amplitude'].value
	sigma  = out.params['L'+str(curva)+'sigma'].value
	area   = amplitude/(sigma*np.pi)

	amplitude_err = out.params['L'+str(curva)+'amplitude'].stderr
	sigma_err  = out.params['L'+str(curva)+'sigma'].stderr

	err_area= np.sqrt(amplitude**2+sigma**2)
	#data_energy_item.write("%s \t \t L%i" %(filename, curva))
	data_energy_item.write("%f \t %f \t" 	 %(out.params['L'+str(curva)+'center'].value,out.params['L'+str(curva)+'center'].stderr))
	data_energy_item.write(" \t %f \t %f \t" %(out.params['L'+str(curva)+'fwhm'].value,out.params['L'+str(curva)+'fwhm'].stderr))
	data_energy_item.write(" \t %f \t %f \n" %(area, err_area))

#cosas que le hago
def per_peak(index):
	
	#Las nuevas semillas para el siguiente fit
	amplitude[index]= out.params['L'+str(index)+ 'amplitude'].value
	sigma[index]=out.params['L'+str(index)+ 'sigma'].value
	center[index]= out.params['L'+str(index)+ 'center'].value
	
	#Imprimo para llevar un control por la terminal
	print(" C{0}={1}, Sigma{0}={2}".format(index,center[index],sigma[index]) )
	plt.annotate("L"+str(index), xy=(center[index],amplitude[index]+c), xytext=(center[index],amplitude[index]+c), horizontalalignment='center', verticalalignment='bottom', rotation=90)

	print_to_fit_log(filename,data_energy_list[index], out, index) 	#Imprimo al fit log
	
#######################Aca podemos agregar curvas###########################3
#Mis archivos 
direc="./twin_peaks/"
files = os.listdir(direc)
files.sort() #Los ordena

#Crea los archivos log 
fit_log= open("./fit_peaks_09_Mayo_04.log", "a+")

data_energy_list = [open("./L0_09_Mayo_04_twin_peaks.txt", "w+"), 
					open("./L1_09_Mayo_04_twin_peaks.txt", "w+"),
					open("./L2_09_Mayo_04_twin_peaks.txt", "w+")]
					#open("./L3_09_Mayo_04.txt", "w+"), 
					#open("./L4_09_Mayo_04.txt", "w+"), 
					#open("./L5_09_Mayo_04.txt", "w+")] 
					#Acá pode4os definir un archivo más

#Nombro las curvas que voy a utilizar

L0_mod=LorentzianModel(prefix="L0")
L1_mod=LorentzianModel(prefix="L1")
L2_mod=LorentzianModel(prefix="L2") 
L3_mod=LorentzianModel(prefix="L3")
L4_mod=LorentzianModel(prefix="L4")
L5_mod=LorentzianModel(prefix="L5")
#4L3_mod=LorentzianModel(pr4fix="L3") 
c_mod=LinearModel()
#c_mod=ConstantModel()

#Semillas antes del primer fit
#center=		[1239.8/809.3,		1239.8/810.2,		1239.8/811.3] #agrego más semillas de ser necesario
center=		[1.53372,1.53395, 1.53591, 1.53447,1.53528,1.53618]  #agrego más semillas de ser necesario
amplitude=	[5000,		1000,		10000, 800,		1400,		3000	 ]
sigma= 		[0.0005115, 	0.0000515, 	0.00005, 0.00001115, 	0.0000115, 	0.00005]

c=800 # la constante
slope=1000

#Cosas que tengo que hacer con los archivos
header_f= lambda x: data_energy_list[x].write("\n#Centro \t err \t \t \t\t  Fwhm \t err \t\t\t\t Area \t Err\n")
flush_f = lambda x: data_energy_list[x].flush()
close_f = lambda x: data_energy_list[x].close()

header_f(0), header_f(1), header_f(2)#, header_f(3), header_f(4), header_f(5)
#acá iria un header_f(3) e.g


##########################Filtro!!!!!
filtro_3=396.45
filtro_2=21.38
filtro_1=8.1
negro= 20.1
filtro_feno=350000

filtro=np.array([filtro_3, filtro_3*filtro_1,filtro_3*filtro_2*filtro_1 ])

#inicial
filtro_total=filtro_3

a= 877.541 
#########################################################################
yes=input("Ver los graficos? [y/n]")

counter=1

for filename in files:
	x,y = np.loadtxt(direc + filename, unpack=True)
	x=1239.8/x

	if counter==5:
		filtro_total=filtro_3*filtro_2*filtro_1#*filtro_feno

	y=(y-a)*filtro_total


	#Imprimo para llevar un control por la terminal
	print(filename)
	
	#Semillas que se dan iterativamente
	pars= L0_mod.make_params(center=center[0], amplitude= amplitude[0], sigma=sigma[0]) 
	pars+=L1_mod.make_params(center=center[1], amplitude= amplitude[1], sigma=sigma[1])
	pars+=L2_mod.make_params(center=center[2], amplitude= amplitude[2], sigma=sigma[2])
	#pars+=L3_mod.make_params(center=center[3], amplitude= amplitude[3], sigma=sigma[3])
	#pars+=L4_mod.make_params(center=center[4], amplitude= amplitude[4], sigma=sigma[4])
	#pars+=L5_mod.make_params(center=center[5], amplitude= amplitude[5], sigma=sigma[5])
	
	pars+=c_mod.make_params(intercept=c, slope=slope)
	#pars+=c_mod.make_params(c=c)

	#Defino funcion
	mod =L0_mod + c_mod + L1_mod + L2_mod# +L3_mod+L4_mod+L5_mod #+L3_mod
	#Fiteo
	out = mod.fit(y, pars, x=x)

	#Imprimo el archivo fit log
	fit_log.write("\n\n\n\n\n\n Fitted from: %s %s \n" %("./19-04-26/", filename))
	now= datetime.datetime.now()
	fit_log.write("At: %i/%i/%i, %i:%i:%i \n" %(now.day,now.month,now.year,now.hour,now.minute,now.second))
	fit_log.write(out.fit_report(min_correl=0.2))

	#A veces no aporta nada plottear si sabemos que fitea
	#yes==1 printea y bueno lo otro no
	if yes=="y":
		plt.subplot(121)
		plt.plot(x, y, 'b', label="Datos") # Datos en azul
		plt.plot(x, out.init_fit, 'g--', label="Semilla") #Plot de la semilla
		plt.plot(x, out.best_fit,'r',label="Ajuste") #Fit en rojo4
		plt.legend(loc='upper left', ncol=1)
		plt.xlabel(u"Energía [eV]")
		plt.ylabel(u"Intensidad [u.a.]")
		plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	
		per_peak(0), per_peak(1), per_peak(2)#, 		per_peak(3), per_peak(4), per_peak(5)
		c=out.params['intercept'].value
		slope=out.params['slope'].value
		#c=out.params['c'].value
		print("C={0}, slope={1}\n".format(c,slope))

	
		plt.subplot(122) #
		plt.plot(x, y - out.best_fit, 'black') # Datos en azul
		plt.show()
		#subprocess.call("python plot_26_abril.py", shell=True)
	elif yes=="n":
		per_peak(0), per_peak(1)#, per_peak(2)
		c=out.params['intercept'].value
		slope=out.params['slope'].value
	

	
	fit_log.flush() 
	flush_f(0), flush_f(1), flush_f(2)#,	flush_f(3), flush_f(4), flush_f(5) #Agrego mas files de ser necesario

	counter+=1

#Aguante Tapia vieja
fit_log.close()
close_f(0), close_f(1), close_f(2)#, close_f(3), close_f(4), close_f(5) #Agrego mas files de ser necesario