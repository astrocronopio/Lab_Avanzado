import numpy as np 
from lmfit.models import LorentzianModel, ConstantModel
from lmfit.model import save_modelresult
from lmfit import minimize, Parameters 
import datetime
import sys
import matplotlib.pyplot as plt
import os

def print_to_fit_log(filename,data_energy, out, curva):
	center = out.params['L'+str(curva)+'amplitude'].value
	sigma =out.params['L'+str(curva)+'sigma'].value
	area= center/sigma

	center_err = out.params['L'+str(curva)+'amplitude'].stderr
	sigma_err = out.params['L'+str(curva)+'sigma'].stderr

	err_area= np.sqrt(center**2+sigma**2)
	data_energy.write("%f \t \t L%i" %(float(filename), curva))
	data_energy.write(" \t \t  %f \t %f \t" %(out.params['L'+str(curva)+'center'].value,out.params['L'+str(curva)+'center'].stderr))
	data_energy.write(" \t \t  %f \t %f \t" %(out.params['L'+str(curva)+'fwhm'].value,out.params['L'+str(curva)+'fwhm'].stderr))
	data_energy.write(" \t \t  %f \t %f \n" %(area*np.pi, err_area))

direction = sys.argv[1]
files = os.listdir(direction)
for x in files:
	x=float(x)
	pass
files.sort()

#fit_log= open("./fit_80K_RT.log", "a+")
data_energy = open("./fit_energy_RT.log", "a+")

now= datetime.datetime.now()
data_energy.write("\n\nAt: %i/%i/%i, %i:%i:%i \n" %(now.day,now.month,now.year,now.hour,now.minute,now.second))
data_energy.write("Archivo \t  Curva \t \t  Centro \t err \t \t \t\t  Fwhm \t err \t\t\t\t Area \t Err\n")


L0_mod=LorentzianModel(prefix="L0")
L1_mod=LorentzianModel(prefix="L1")
L2_mod=LorentzianModel(prefix="L2")
L3_mod=LorentzianModel(prefix="L3")
L4_mod=LorentzianModel(prefix="L4")
L5_mod=LorentzianModel(prefix="L5")
c_mod=ConstantModel()

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
center= 842.5
center1= 815
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
	
	pars= L0_mod.make_params(center=center+1.0, amplitude=amplitude, sigma=sigma) 
	pars+=L1_mod.make_params(center=center1, amplitude= amplitude1, sigma=sigma1)
	pars+=L2_mod.make_params(center=center2, amplitude= amplitude2, sigma=sigma2, max=2*sigma2 )
	pars+=c_mod.make_params(c=c)

	mod =L0_mod + c_mod + L1_mod + L2_mod

	#Aparecen picos extra a partir de estos archivos
	if float(filename)>=20.50:
		if float(filename)==20.50:
			pars+=L3_mod.make_params(center= center1-0.5, amplitude= amplitude1, sigma=sigma1)
			pars+=L4_mod.make_params(center=center2-1.5, amplitude= amplitude2, sigma=sigma2)
		else:
			pars+=L3_mod.make_params(center= center3, amplitude= amplitude3, sigma=sigma3)
			pars+=L4_mod.make_params(center=center4, amplitude= amplitude4, sigma=sigma4)

		mod +=L3_mod + L4_mod
		pass

	if float(filename)>=23.00 and float(filename)<=25.00:
		if float(filename)==23.00:
			pars+=L5_mod.make_params(center= center4-1.5, amplitude= amplitude4, sigma=sigma1)
		else:
			pars+=L5_mod.make_params(center= center5, amplitude= amplitude5, sigma=sigma5)
		mod+=L5_mod
		pass

	#pars['L0sigma'].max=8
	#Fit de las curvas
	now= datetime.datetime.now()
	out = mod.fit(y, pars, x=x)

	#fit_log.write("\n\n\n Fitted from: %s%s \t" %(direction, filename))
	#fit_log.write("At: %i/%i/%i, %i:%i:%i \n" %(now.day,now.month,now.year,now.hour,now.minute,now.second))
	#fit_log.write(out.fit_report(min_correl=0.2))

	print_to_fit_log(filename,data_energy, out, 0)
	print_to_fit_log(filename,data_energy, out, 1)
	print_to_fit_log(filename,data_energy, out, 2)

	center = out.params['L0center'].value #+ 0.1  if center < out.params['L0center'].value else out.params['L0center'].value 
	center1= out.params['L1center'].value 
	center2= out.params['L2center'].value +0.1 if center2 < out.params['L2center'].value else out.params['L2center'].value -0.1

	amplitude = out.params['L0amplitude'].value
	amplitude1= out.params['L1amplitude'].value
	amplitude2= out.params['L2amplitude'].value

	sigma =out.params['L0sigma'].value
	sigma1=out.params['L1sigma'].value
	sigma2=out.params['L2sigma'].value

	c=out.params['c'].value

	if float(filename)>=20.50:
		center3= out.params['L3center'].value 
		center4= out.params['L4center'].value #+0.1 if center2 < out.params['L2center'].value else out.params['L2center'].value -0.1
	
		print_to_fit_log(filename, data_energy, out, 3)
		print_to_fit_log(filename, data_energy, out, 4)

		amplitude3= out.params['L3amplitude'].value
		amplitude4= out.params['L4amplitude'].value
	
		sigma3=out.params['L3sigma'].value
		sigma4=out.params['L4sigma'].value
		pass

	if float(filename)>=23.00 and float(filename)<=25.00:
		center5= out.params['L5center'].value #+0.1 if center2 < out.params['L2center'].value else out.params['L2center'].value -0.1
		amplitude5= out.params['L5amplitude'].value
		sigma5=out.params['L5sigma'].value

		print_to_fit_log(filename, data_energy, out, 5)
		pass

	print(filename)
	print(" C=  %f, Sigma = %f" % (center, sigma))
	print(" C1= %f, Sigma1= %f" % (center1, sigma1))
	print(" C2= %f, Sigma2= %f" % (center2, sigma2))

	plt.plot(x, y, 'b.')
	plt.plot(x, out.init_fit, 'g--')
	plt.plot(x, out.best_fit, 'r')
	plt.show()

	#fit_log.flush()
	data_energy.flush()

#fit_log.close()
data_energy.close()