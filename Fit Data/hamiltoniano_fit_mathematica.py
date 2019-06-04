import numpy as np

x, low, med, high = np.loadtxt("./diagonalizar_eV.txt", unpack=True)
energy=[low, med, high]

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
Rabbi_lh= 0.0019265
Rabbi_hh= 0.0029826
###################################3

eigenvalues_file=open("./eigenvalues.txt", "w+")
eigenvector_LP=open("./eigenvectors_LP.txt", "w+")
eigenvector_MP=open("./eigenvectors_MP.txt", "w+")
eigenvector_UP=open("./eigenvectors_UP.txt", "w+")


from numpy import linalg as LA

def cavity(x,a,b,c):
	return a+b*x+c*x**2

def return_eigenvalues(x):
	Matrix = np.array([	[cavity(x,A,B,C),		Rabbi_hh		,		Rabbi_lh			]	,\
						[Rabbi_hh		,		x*slope_hh+ hh	,			0				]	,\
						[Rabbi_lh		,		0				, 		x*slope_lw+lw		]	])

	eigenvalues, vectors = LA.eig(Matrix)
	return eigenvalues, vectors

energy_fit=[[],[],[]]

for position in x:
	eigenvalues, eigenvectors=return_eigenvalues(position)

	eigenvector_MP.write("%f \t %f \t %f \t %f \n" %(position,eigenvectors[0][0]**2,eigenvectors[0][1]**2,eigenvectors[0][2]**2))
	eigenvector_LP.write("%f \t %f \t %f \t %f \n" %(position,eigenvectors[1][0]**2,eigenvectors[1][1]**2,eigenvectors[1][2]**2))
	eigenvector_UP.write("%f \t %f \t %f \t %f \n" %(position,eigenvectors[2][0]**2,eigenvectors[2][1]**2,eigenvectors[2][2]**2))

	eigenvalues.sort()
	eigenvalues_file.write("%f \t %f \t %f \t %f \n" %(position, eigenvalues[0],eigenvalues[1],eigenvalues[2]))
	pass