import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

#mpl. params es para cambiar el tamaño de la letra#####
import matplotlib as mpl
mpl.rcParams.update({'font.size': 22,  'figure.figsize': [12, 8],  'figure.autolayout': True})
#######################################################

def lineal_angulo(x, x_0,E_0):
	NA= 0.582364238 
	c= 299792458
	h= 4.13E-15


	m= 2*NA/103

	return E_0*np.tan(m*(x-x_0))/(c*h)

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

def para_energia(y,y0,E0, y2, E2):
	m= (E0-E2)/(y0-y2)
	return m*(y-y0) + E0

def para_plotear_rotado(data, puntos):
	#Quita la nube de puntos que se tiene
	data=suaviza(data)
	#rota la imagen en  un ángulo muy pequeño
	data=girar(data)
	data=np.array(data)

	x0, y0, E0, y2, E2 = puntos[0], puntos[1], puntos[2], puntos[3], puntos[4]

	x_rot=data[:,0]
	y_rot=data[:,1]

	x_rot= lineal_angulo(x_rot, x0, E0)
	y_rot= para_energia(y_rot,)

	#Hace el fit
	#fit_params_rot, pcov= scipy.optimize.curve_fit(parabola, x_rot[15:-12],y_rot[15:-12])

	#print(fit_params_rot)
	y_fit_rot = []
	#for x in x_rot:
	#	y_fit_rot.append(parabola(x, *fit_params_rot))

	return x_rot, y_rot, y_fit_rot

def plotea_el_archivo(data, colores, name, puntos, si=0):
	x_rot, y_rot, y_fit_rot=para_plotear_rotado(data,puntos)

	plt.plot(x_rot, y_rot,label=name, c=colores)


#Cavidad 1
#			x0,     y0,  	E0, 	y2, 	E2 
puntos=[		,		,		,		,		]
data_cavidad = np.loadtxt("20190314_vuelta_sobre_la_muestra/text_files/trash/fainstein_dream_6_cavity_mode.txt")

#CAvidad 2
#			x0,     y0,  	E0, 	y2, 	E2 
