import numpy as np 
from lmfit.models import LorentzianModel, ConstantModel
from lmfit.model import save_modelresult
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

#fit_log= open("./fit_simple_lorentzian.log", "a+")
data_energy = open("./fit_simple_lorentzian_energy.log", "a+")
now= datetime.datetime.now()
data_energy.write("\n\nAt: %i/%i/%i, %i:%i:%i \n" %(now.day,now.month,now.year,now.hour,now.minute,now.second))
data_energy.write("Archivo \t  Curva \t \t  Centro \t err \t \t \t\t  Fwhm \t err \t\t\t\t Area \t Err\n")

L_mod=LorentzianModel(prefix='L0')
c_mod=ConstantModel()

for filename in files:
	x,y = np.loadtxt(direction + filename, unpack=True)
	
	pars=L_mod.guess(y, x=x)
	pars+=c_mod.guess(y, x=x)
	
	mod =L_mod + c_mod
	out = mod.fit(y, pars, x=x)

#	fit_log.write("\n\n\n\n\n\n Fitted from: %s%s \n" %(direction, filename))
#	now= datetime.datetime.now()
#	fit_log.write("At: %i/%i/%i, %i:%i:%i \n" %(now.day,now.month,now.year,now.hour,now.minute,now.second))
#	fit_log.write(out.fit_report(min_correl=0.2))

	print_to_fit_log(filename, data_energy, out, 0)
	
	plt.plot(x, y, 'b')
	plt.plot(x, out.init_fit, 'g--')
	plt.plot(x, out.best_fit, 'r')
	plt.show()