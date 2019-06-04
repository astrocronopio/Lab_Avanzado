"""Este script esta hecho para fitear un lorentziana o un Voigt, graficas el fit y data
ademas de mostrar los residuos, imprime un archivo por cada pico, y ese archivo van 
el centro, ancho, area y sus errores
para agregar más curvas, falta poner mas files output y definir un pico más
EL SCRIPT BORRA LOS ARCHIVOS ANTERIORES!
"""
import numpy as np 
from lmfit.models import LorentzianModel, LinearModel,  VoigtModel 
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
	print_to_fit_log(filename,data_energy_list[index], out, index) 	#Imprimo al fit log
	
	#Las nuevas semillas para el siguiente fit
	amplitude[index]= out.params['L'+str(index)+ 'amplitude'].value
	sigma[index]=out.params['L'+str(index)+ 'sigma'].value
	center[index]= out.params['L'+str(index)+ 'center'].value
	
	#Imprimo para llevar un control por la terminal
	print(" C{0}={1}, Sigma{0}={2}".format(index,center[index],sigma[index]) )
	plt.annotate("L"+str(index), xy=(center[index],amplitude[index]+c), xytext=(center[index],amplitude[index]+c), horizontalalignment='center', verticalalignment='bottom', rotation=90)

#######################Aca podemos agregar curvas###########################3
#Mis archivos 
directory= "/home/ponci/Dropbox/IB/Cuarto_Semestre/Experimental/Nitrogeno/LT/"
files = os.listdir(directory)
files.sort() #Los ordena

#Crea los archivos log 
fit_log= open("./fit_peaks_LT.log", "a+")

data_energy_list = [open("./L0_LT.txt", "w+"), 
					open("./L1_LT.txt", "w+"), 
					open("./L2_LT.txt", "w+")] 
					#Acá podemos definir un archivo más

#Nombro las curvas que voy a utilizar

L0_mod=LorentzianModel(prefix="L0")
L1_mod=LorentzianModel(prefix="L1")
L2_mod=LorentzianModel(prefix="L2") 
# L3_mod=LorentzianModel(prefix="L3") 
c_mod=LinearModel()

#Semillas antes del primer fit
#center=		[1239.8/809.3,		1239.8/810.2,		1239.8/811.3] #agrego más semillas de ser necesario
center=		[1.52316,1.52913,1.54431] #agrego más semillas de ser necesario
amplitude=	[0.1,		0.1,			0.1	 ]
sigma= 		[0.0000915, 		0.0000915, 		0.0000915]

c=877.541  # la constante
slope=0.0001

#Cosas que tengo que hacer con los archivos
header_f= lambda x: data_energy_list[x].write("\n#Centro \t err \t \t \t\t  Fwhm \t err \t\t\t\t Area \t Err\n")
flush_f = lambda x: data_energy_list[x].flush()
close_f = lambda x: data_energy_list[x].close()

header_f(0), header_f(1), header_f(2) #acá iria un header_f(3) e.g


##########################Filtro!!!!!
filtro_3=396.45
filtro_2=21.38
filtro_1=8.1

filtro=np.array([filtro_3, filtro_3*filtro_1,filtro_3*filtro_2*filtro_1 ])/filtro_3

#inicial
filtro_total=filtro[0]

a= 877.541 
#########################################################################
yes=input(u"¿Queres ver los gráficos? [y/n]")

counter=0

for filename in files:
	x,y = np.loadtxt(directory + filename, unpack=True)
	x=1239.8/x

	#Imprimo para llevar un control por la terminal
	print(filename)
	
	#Semillas que se dan iterativamente
	pars= L0_mod.make_params(center=center[0], amplitude= amplitude[0], sigma=sigma[0]) 
	pars+=L1_mod.make_params(center=center[1], amplitude= amplitude[1], sigma=sigma[1])
	pars+=L2_mod.make_params(center=center[2], amplitude= amplitude[2], sigma=sigma[2])
		#pars+=L3_mod.make_params(center=center[3], amplitude= amplitude[3], sigma=sigma[3])
	pars+=c_mod.make_params(intercept=c, slope=slope)

	#Defino funcion
	mod =L0_mod + c_mod + L1_mod + L2_mod #+L3_mod
	#Fiteo
	out = mod.fit(y, pars, x=x)

	#Imprimo el archivo fit log
	fit_log.write("\n\n\n\n\n\n Fitted from: %s %s \n" %(directory, filename))
	now= datetime.datetime.now()
	fit_log.write("At: %i/%i/%i, %i:%i:%i \n" %(now.day,now.month,now.year,now.hour,now.minute,now.second))
	fit_log.write(out.fit_report(min_correl=0.2))

	#A veces no aporta nada plottear si sabemos que fitea
	#yes==1 printea y bueno lo otro no
	if yes=="y":
		plt.subplot(121)
		plt.plot(x, y, 'b', label="Datos") # Datos en azul
		plt.plot(x, out.init_fit, 'g--', label="Semilla") #Plot de la semilla
		plt.plot(x, out.best_fit,'r',label="Fit") #Fit en rojo4
		plt.legend(loc='upper left', ncol=1)
	
		per_peak(0), per_peak(1), per_peak(2)
		c=out.params['intercept'].value
		slope=out.params['slope'].value
	
		plt.subplot(122) #
		plt.plot(x, y - out.best_fit, 'black') # Datos en azul
		plt.show()
		#subprocess.call("python plot_LT.py", shell=True)
	elif yes=="n":
		per_peak(0), per_peak(1), per_peak(2)
		c=out.params['intercept'].value
		slope=out.params['slope'].value
	
	
	fit_log.flush() 
	flush_f(0), flush_f(1), flush_f(2) #Agrego mas files de ser necesario

	counter+=1

#Aguante Tapia vieja
fit_log.close()
close_f(0), close_f(1), close_f(2) #Agrego mas files de ser necesario