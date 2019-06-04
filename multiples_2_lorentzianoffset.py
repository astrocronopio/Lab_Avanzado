import numpy as np 
from lmfit.models import LorentzianModel, ConstantModel
from lmfit import minimize, Parameters 
import datetime
import sys
import matplotlib.pyplot as plt
import os

def print_to_fit_log(filename,data_energy, out, curva):
	center = out.params['L'+str(curva)+'amplitude'].value
	sigma =out.params['L'+str(curva)+'sigma'].value
	area= center/(sigma*np.pi)

	center_err = out.params['L'+str(curva)+'amplitude'].stderr
	sigma_err = out.params['L'+str(curva)+'sigma'].stderr

	err_area= np.sqrt(center**2+sigma**2)
	data_energy.write("%f \t \t L%i" %(float(filename), curva))
	data_energy.write(" \t \t  %f \t %f \t" %(out.params['L'+str(curva)+'center'].value,out.params['L'+str(curva)+'center'].stderr))
	data_energy.write(" \t \t  %f \t %f \t" %(out.params['L'+str(curva)+'fwhm'].value,out.params['L'+str(curva)+'fwhm'].stderr))
	data_energy.write(" \t \t  %f \t %f \n" %(area, err_area))

#Mis archivos tienen el nombre de un dato por eso los paso a float
direction = sys.argv[1]
files = os.listdir(direction)
for x in files:
	x=float(x)
	pass
#Los ordena
files.sort()

#Crea los archivos log 
fit_log= open("./fit_80K_LT.log", "a+")
data_energy = open("./fit_energy_LT.log", "a+")

now= datetime.datetime.now()
fit_log.write("\n\nAt: %i/%i/%i, %i:%i:%i \n" %(now.day,now.month,now.year,now.hour,now.minute,now.second))
data_energy.write("Archivo \t  Curva \t \t  Centro \t err \t \t \t\t  Fwhm \t err \t\t\t\t Area \t Err\n")

#Nombro las curvas que voy a utilizar
L0_mod=LorentzianModel(prefix="L0")
L1_mod=LorentzianModel(prefix="L1")
L2_mod=LorentzianModel(prefix="L2")
c_mod=ConstantModel()
c2_mod=ConstantModel(prefix="L2")

#Semillas antes del primer fit
'''	
%Hasta la mitad de los datos
center= 814
center1= 811.5
center2= 809

amplitude= 5000
amplitude1= 1000
amplitude2= 1000

sigma=0.13
sigma1=0.83
sigma2= 1.38

c=856.0
'''
center= 812.5	
center1= 810
center2= 810.5

amplitude= 5000
amplitude1= 300
amplitude2= 300

sigma=0.4
sigma1=0.15
sigma2= 0.4

c=856.0

for filename in files:
	x,y = np.loadtxt(direction + filename, unpack=True)

	inicio= ind= list(abs(x-805)).index(np.nanmin(abs(x-805)))
	ind= list(abs(x-815)).index(np.nanmin(abs(x-815)))
	cavity_y=y[ind:]
	cavity_x=x[ind:]

	y=y[inicio:ind]
	x=x[inicio:ind]


	#Semillas que se dan iterativamente
	pars= L0_mod.make_params(center=center,  amplitude= amplitude, sigma=sigma) 
	pars+=L1_mod.make_params(center=center1, amplitude= amplitude1, sigma=sigma1)

	pars2=L2_mod.guess(cavity_y, x= cavity_x)
	pars+=c_mod.make_params(c=c)
	pars2+=c2_mod.make_params(c=c)


	#bound_parameters_sigma(pars,2,5)

	#Defino funcion
	mod =L0_mod + c_mod + L1_mod #+  L2_mod
	mod2 = L2_mod + c2_mod 
	#Fiteo
	out = mod.fit(y, pars, x=x)
	out_cavity= mod2.fit(cavity_y, pars2, x=cavity_x)

	#Imprimo el archivo fit log
	fit_log.write("\n\n\n\n\n\n Fitted from: %s%s \n" %(direction, filename))
	now= datetime.datetime.now()
	fit_log.write("At: %i/%i/%i, %i:%i:%i \n" %(now.day,now.month,now.year,now.hour,now.minute,now.second))
	fit_log.write(out.fit_report(min_correl=0.2))

	#Imprimo al fit log
	print_to_fit_log(filename,data_energy, out, 0)
	print_to_fit_log(filename,data_energy, out, 1)
	print_to_fit_log(filename,data_energy, out_cavity, 2)
	
	#Las nuevas semillas para el siguiente fit
	amplitude= out.params['L0amplitude'].value
	amplitude1= out.params['L1amplitude'].value
	amplitude2= out_cavity.params['L2amplitude'].value

	sigma=out.params['L0sigma'].value
	sigma1=out.params['L1sigma'].value
	sigma2= out_cavity.params['L2sigma'].value

	center= out.params['L0center'].value #+ 0.1  if center < out.params['center'].value else out.params['center'].value 
	center1= out.params['L1center'].value 
	center2= out_cavity.params['L2center'].value +0.1 if center2 < out_cavity.params['L2center'].value else out_cavity.params['L2center'].value -0.1

	c=out.params['c'].value

	#Imprimo para llevar un control por la terminal
	print(filename)
	print(" C0= %f, Sigma0= %f" % (center, sigma))
	print(" C1= %f, Sigma1= %f" % (center1, sigma1))
	#print(" C2= %f, Sigma2= %f" % (center2, sigma2))


	plt.plot(x, y, 'b') # Datos en azul
	plt.plot(cavity_x, cavity_y, 'black') # Datos en azul
	plt.plot(x, out.init_fit, 'g--') #Plot de la semilla
	plt.plot(x, out.best_fit, 'r') #Fit en rojo
	plt.plot(cavity_x, out_cavity.best_fit, 'y-')
	plt.show()

	fit_log.flush() 
	data_energy.flush()

#Aguante Tapia vieja
fit_log.close()
data_energy.close()