#encoding=utf-8
import numpy as np
import matplotlib.pyplot as plt


import matplotlib as mpl
mpl.rcParams.update({'font.size':24,  'figure.figsize': [10, 6],  'figure.autolayout': True})

filtro_3=396.45
filtro_2=21.38
filtro_1=8.1

espectro="./espectro/084.txt"
espectro1="./espectro/077.txt"
x,y = np.loadtxt(espectro, unpack=True)
x1,y1=np.loadtxt(espectro1, unpack=True)
y=(y-875)*filtro_2
y1=(y1 -875)*10


y1=y1/y.max()
y=y/y.max()

plt.plot(1239.84/x1,y1, marker="s"  , label="8.3 mW (x10)")#\n$1.6\\times1.6\\,\\mu$m")
plt.plot(1239.84/x,y,   marker="^"  , label="15.4 mW")#\n$1.6\\times1.6\\,\\mu$m")

plt.xlabel(u"Energía [eV]")
plt.ylabel(u"Intensidad [u.a.]")
plt.grid(alpha=0.4)
plt.legend()
plt.xlim(1.531,1.537)
plt.show()