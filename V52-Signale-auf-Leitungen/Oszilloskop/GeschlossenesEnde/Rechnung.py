import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.stats import norm #Nur hier, um fehlerbehaftete Daten zu erzeugen


x, y  = np.genfromtxt('F0049CH1.txt', unpack=True)

#den zu plottenden bereich heraussuchen (und nur jeden 4. wert nehmen):
x_plot = np.zeros(400)
y_plot = np.zeros(400)


#bereich auswählen und in Megahertz umrechen
for i in range(0, 400):
	x_plot[i] = x[1600+i]*10**9
	y_plot[i] = y[1600+i]


###Regression:

#Funktion definieren
def spannung(x, a, b, c, d, e):
    return 2*a*(1+b-b*np.exp(-c*(x-d))) + e

#Rechnung ohne Berücksichtigung eines Fehlers in y-Richtung
params, cov = curve_fit(spannung, x_plot, y_plot, (-2.72, 0.379, 1, 500, 1.5))
print(params)
print(cov)


#plt.plot(x_plot, spannung(x_plot, 10, 1, 10**6, 10**(-7), -10), 'b-')
#plt.errorbar(x_vector, model(x_vector, params[0], params[1]), yerr=..., xerr=..., )
plt.plot(x_plot, y_plot, 'rx')
plt.plot(x_plot, spannung(x_plot, *params))

#print(x_plot)





plt.ylim(-10,0)

plt.show()
plt.savefig('plot.pdf')
plt.close()





#plt.xlim(x_plot[0],x_plot[399])
plt.show()
plt.close()

x = np.linspace(400,410)
plt.plot(x, spannung(x,-2.72, 0.379, 1, 400, 1.5))
#plt.xlim(x_plot[0],x_plot[399])
plt.show()

