import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

#mpl. params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 22,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################

def suaviza(data):
	#Ya tiene en cuenta que la segunda columna se repite
	new_data=[]
	
	previous=data[0]
	counter=0
	sum_=0
	for x in  data[1:]:
		if previous[1]==x[1]:
			sum_+=x[0]
			counter+=1
			pass
		else:
			meaan= sum_/counter if counter!=0 else sum_
			new_data.append([meaan,previous[1]])
			sum_=0
			counter=0
			previous=x
			pass
		pass
	return new_data

def parabola(x,a,b,c):
	return a*x**2 + b*x + c

def girar(new_data_cavidad):
	#Vamos a girar la imagen
	new_data_cavidad_rotado=[]

	A= [	[1			  ,	-11.55/846.096],
			[11.55/846.096, 			 1]]
	
	#Gorda pelotuda, acá se intercambian las columnas
	for x in new_data_cavidad:
		rotado = np.matmul(A,[x[1], x[0]])
		new_data_cavidad_rotado.append([rotado[0],rotado[1]])
		pass

	return new_data_cavidad_rotado

def para_plotear_rotado(data):
	#Quita la nube de puntos que se tiene
	new_data=suaviza(data)

	#rota la imagen en  un ángulo muy pequeño
	new_data_rotado=girar(new_data)

	new_data_rotado=np.array(new_data_rotado)

	x_rot=new_data_rotado[:,0]
	y_rot=new_data_rotado[:,1]

	#Hace el fit
	fit_params_rot, pcov= scipy.optimize.curve_fit(parabola, x_rot[15:-10],y_rot[15:-10])

	#aux=list(filter(lambda x: a<x[0]<b, datos))

	print(fit_params_rot)

	y_fit_rot = []
	for x in x_rot:
		y_fit_rot.append(parabola(x, *fit_params_rot))

	return x_rot, y_rot, y_fit_rot

def plotea_el_archivo(data, c, name, recta, offset, e_0, si=0, rango=0):

	x_, y_, y_fit_ = para_plotear_rotado(data)
	
	x_, y_, y_fit_ = np.array(x_) , np.array(y_), np.array(y_fit_) #casteo a numpy array porque python no es perfecto
	
	test= girar(data)
	test= np.array(test)
	x,y = test[:,1], test[:,0]

	z=  lineal_angulo(x_,offset,e_0)

	plt.plot(z/1000000, recta(y_), color=c, label=name)
	#if si==1 :
	#	plt.plot(z/1000000, recta(y_fit_), '--', color='black', label='Ajuste')
	#else:
	#	plt.plot(z/1000000, recta(y_fit_), '--', color='black')
	#
	plt.plot(0.000001*lineal_angulo(y, offset, e_0),recta(x), '.', color=c)

	plt.grid(alpha=0.4)
	plt.ylabel("Energía [eV]")
	plt.xlabel("k$_{\parallel}$ [$\mu$m$^{-1}$]")
	plt.legend(loc='center',handler_map={})
	plt.ylim(1.502,1.525)
	if rango==1:
		plt.xlim(-0.3,0.3)

def recta_energia_cruce(x):
	return 1.5341-1.9318*x/100000


def recta_energia_excitonico(x):
	return 1.52219002875581 -1.87037193415863E-05*x


def lineal_angulo(x, x_0,E_0):
	NA= 0.582364238 
	c= 299792458
	h= 4.13E-15


	m= 2*NA/(103)

	return E_0*np.tan(m*(x-x_0))/(c*h)




###Gráfico para el cruce

data_LP=np.loadtxt("20190314_vuelta_sobre_la_muestra/text_files/trash/casi_cruce_LP.txt")
#data_MP=np.loadtxt("20190314_vuelta_sobre_la_muestra/text_files/casi_cruce_MP.txt")
#data_UP=np.loadtxt("20190314_vuelta_sobre_la_muestra/text_files/casi_cruce_UP_.txt")
data_cavidad = np.loadtxt("20190314_vuelta_sobre_la_muestra/text_files/trash/fainstein_dream_6_cavity_mode.txt")
#data_exciton = np.loadtxt("20190314_vuelta_sobre_la_muestra/text_files/fainstein_dream_6_modo_excitonico_solamente.txt")
#data_cavidad_1=np.loadtxt("cavidad/cavidad_1_51.txt")
#data_cavidad_2=np.loadtxt("cavidad/super_lindo_LP_1_51534.txt")

plt.figure(0)
#plotea_el_archivo(data_UP, 'brown', 'UP (anticruce)', recta_energia_cruce, 139.585774693775 , 1.51911)
#plotea_el_archivo(data_MP, 'red', 'MP (anticruce)', recta_energia_cruce, 135.552338090164 , 1.52210)
plotea_el_archivo(data_LP, 'blue', 'LP ($\delta = 19\,$mEv)', recta_energia_cruce, 135.24079 , 1.52648,0,1)
#plotea_el_archivo(data_cavidad_1, 'red', 'LP ($\delta = -10$)', recta_energia_cruce,135.3,1.51)
#plotea_el_archivo(data_cavidad_2, 'red', 'LP ($\delta = -1.5$)', recta_energia_cruce,135.3,1.51534)
plotea_el_archivo(data_cavidad, 'green', 'LP ($\delta = -18.8\,$mEv)', recta_energia_excitonico, 135.33785559873,1.50434,1,1)

#Gráfico muy excitónico

plt.figure(2)
plotea_el_archivo(data_cavidad, 'green', 'LP ($\delta = -18.8\,$mEv)', recta_energia_excitonico, 135.33785559873,1.50434,1,1)


plt.figure(1)

data_cavidad = np.loadtxt("20190314_vuelta_sobre_la_muestra/text_files/trash/fainstein_dream_6_cavity_mode.txt")
#data_exciton = np.loadtxt("20190314_vuelta_sobre_la_muestra/text_files/fainstein_dream_6_modo_excitonico_solamente.txt")
#plotea_el_archivo(data_exciton, 'yellow', 'Excitón', recta_energia_excitonico, 137.405257689803)
plotea_el_archivo(data_cavidad, 'green', 'LP ($\delta = -18.8\,$mEv)', recta_energia_excitonico, 135.33785559873,1.50434, 1)



plt.show()

## 135.24079864475
#135.552338090164
#139.585774693775


#137.405257689803
#135.33785559873


#fit_LP=[-6.20130089e-02, 1.67733777e+01, -4.04037192e+02]
#fit_MP=[-5.80423061e-02, 1.57355406e+01, -3.93239871e+02]
#fit_UP=[-4.80178823e-02, 1.34052266e+01, -5.51153054e+02]


#fit_exciton=[-3.34558155e-02, 9.19400990e+00, -5.34878916e+02]
#fit_cavidad=[-2.29246460e-01, 6.20514486e+01, -3.24459782e+03]

#LP 1.51911
#MP 1.52210
#UP 1.52648

#Cavity 1.50434
#Exciton 1.52038