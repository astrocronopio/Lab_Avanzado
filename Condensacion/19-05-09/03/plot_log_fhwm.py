#encoding=utf-8
import numpy as np
import matplotlib.pyplot as plt


import matplotlib as mpl
mpl.rcParams.update({'font.size': 30,  'figure.figsize': [12, 9],  'figure.autolayout': True})


file= "mesh_L0.txt"
file_dimi="FWHM_FP.txt"


potencia, center, err_center, \
		    fwhm, err_fw, \
		    intensity, err_intensity, \
		    height, err_height, \
		    			    =  np.loadtxt(file, unpack="True")
y=potencia

potencia_total, fwhm_, err_fw_= np.loadtxt("ancho.txt", unpack="True")

plt.figure(0)
plt.plot(potencia/2.1,center, label="1.6x1.6 $\mu$m (ascending)")
plt.xlabel("Power [mW]")
plt.ylabel("Energy [eV]")
plt.legend(loc='lower right', ncol=1)


fig=plt.figure(1)
plt.title("1.6x1.6 $\mu$m")

pote,FP,erFP,Spec,Sper =np.loadtxt(file_dimi, unpack="True")

print(pote)

ax1 = fig.add_subplot(111)
ax1.set_xticks([5,10,20,30,40,50,60])
ax1.plot([0,150], [0.025, 0.025], c='brown', linestyle='--', lw=5)
area = ax1.plot(potencia_total/2.06,fwhm_*1000, linestyle='--',  marker='^', ms= 8 , c='r', label="FWHM TAS")
#ax1.plot(pote, 1000*FP, marker='o',ms= 8, c='blue', label="FWHM FP")
ax1.tick_params(axis='y', colors='red')
ax1.legend(loc='center right', ncol=1)
ax1.grid(alpha=0.4)




ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
wide = ax2.plot(y/2.06,intensity,  ':', markersize= 8 , marker='s', color='black')
#ax2.yaxis.label.set_color('red')
ax2.set_yscale('log')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")


ax1.set_ylabel(u"FWHM [meV] \u25B4 ")
#ax1.set_ylabel(u"FWHM [meV] \u25B4 ")
ax1.yaxis.label.set_color('red')
ax1.tick_params(axis='y', colors='red')
ax1.set_xlabel(u"Potencia [mW]")
#ax1.set_xlabel(u"Power [mW]")


ax2.set_ylabel(u"Intensidad [u.a.] \u25A0")
#ax2.set_ylabel(u"PL Intensity [a.u.] \u25A0")
ax2.yaxis.label.set_color('black')
ax2.set_xlabel("Potencia [mW]")
#ax2.set_xlabel("Power [mW]")
ax1.set_xlim(7.5,120)
#ax1.set_xticks([20,50,100,150])
#ax2.set_xticks([20,50,100,150])

fig=plt.figure(2)
plt.title("1.6x1.6 $\mu$m")


ax1 = fig.add_subplot(111)
#ax1.set_title(label_fit[x])
area = ax1.plot(potencia/2.06,height, linestyle='--',  marker='^', ms= 8 , c='r')
#ax1.plot(pote, 1000*FP, marker='o',ms= 8, c='blue', label="FP")
ax1.legend(loc='center right', ncol=1)

#ax1.set_xscale('log')
ax1.tick_params(axis='y', colors='red')
#ax1.plot(y, yones*0.025, c='b', linestyle='-', label="LPO")
#ax1.plot(y, yones*0.06, c='r', linestyle='--', label=pdi)
#ax1.legend(loc='center left', ncol=1)

ax1.set_ylabel(u"FWHM [meV] \u25B4 ")
ax1.yaxis.label.set_color('red')
ax1.tick_params(axis='y', colors='red')
ax1.set_xlabel(u"Power [mW]")

plt.show()