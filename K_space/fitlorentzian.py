import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from lmfit.models import GaussianModel, ConstantModel
from lmfit.model import save_modelresult


files=os.listdir("./matrices/")
from matplotlib.colors import ListedColormap

cmap = ListedColormap(['k', 'w', 'r'])
print(files)

matrices=np.zeros((1024,256))

index=0

L_mod=GaussianModel()
c_mod=ConstantModel()


pixel_x= np.arange(1024)

for filename in files:
	data=np.loadtxt("./matrices/"+filename)
	pixel_y= data[:,0]
	data=np.delete(data,0,1)
	maxima=[]
	data=np.log(data)

	for linea in range(len(data)):
		#print(data)
		#print(pixel_x)
		pars=L_mod.guess(data[linea], x=pixel_x)
		pars+=c_mod.guess(data[linea], x=pixel_x)
		
		mod =L_mod + c_mod
		out = mod.fit(data[linea], pars, x=pixel_x)

		print(out.fit_report(min_correl=0.2))

#plt.imshow(np.log(matrices), cmap=cmap)

plt.show()

