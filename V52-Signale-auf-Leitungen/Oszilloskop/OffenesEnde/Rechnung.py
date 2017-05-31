import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.stats import norm #Nur hier, um fehlerbehaftete Daten zu erzeugen


x, y  = np.genfromtxt('F0048CH1.txt', unpack=True)

#den zu plottenden bereich heraussuchen (und nur jeden 4. wert nehmen):
x_plot = np.zeros(50)
y_plot = np.zeros(50)


#bereich auswählen und in Megahertz umrechen
for i in range(0, 50):
	x_plot[i] = x[700+8*i]*10**6
	y_plot[i] = y[700+8*i]


###Regression:

#Funktion definieren
def funktion(x, a, b, c, d, e):
    return 2*a*(1-b*np.exp(-c*(x-d))) + e

#Rechnung ohne Berücksichtigung eines Fehlers in y-Richtung
params, cov = curve_fit(funktion, x_plot, y_plot, (10, 1, 10**6, 1**(-7), -10))
print(params)
print(cov)


plt.plot(x_plot, funktion(x_plot, 10, 1, 10**6, 10**(-7), -10), 'b-')
#plt.errorbar(x_vector, model(x_vector, params[0], params[1]), yerr=..., xerr=..., )
plt.plot(x_plot, y_plot, 'rx')

print(x_plot)



plt.xlabel('...')
plt.ylabel('...')
plt.legend(loc='best')

plt.show()
plt.savefig('plot.png')
