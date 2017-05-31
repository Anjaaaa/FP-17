import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat
import matplotlib.pyplot as plt

from table import (
        make_table,
        make_full_table,
        make_SI,
        write)



#Kapaztät
x, y  = np.genfromtxt('Oszilloskop/Box25/F0051CH1.txt', unpack=True)

#den zu plottenden bereich heraussuchen (und nur jeden 4. wert nehmen):
x_plot = np.zeros(1000)
y_plot = np.zeros(1000)


#bereich auswählen und in Megahertz umrechen
for i in range(0, 1000):
	x_plot[i] = x[571+i]*10**9
	y_plot[i] = y[571+i]


###Regression:

plt.plot(x,y)
plt.show()
plt.close()

#Funktion definieren
def spannung2(x, a, b, c, d, e):
    return 2*a*(1-b*np.exp(-c*(x-d))) + e

#Rechnung ohne Berücksichtigung eines Fehlers in y-Richtung
params, cov = curve_fit(spannung2, x_plot, y_plot, (200, 1, 0.001, 0, -100))
print(params)
print(cov)




#plt.errorbar(x_vector, model(x_vector, params[0], params[1]), yerr=..., xerr=..., )
plt.plot(x*10**9, y,'kx', label = 'Messwerte')
plt.plot(x_plot, spannung2(x_plot, *params), 'r-', linewidth = 2, label = 'Fit-Funktion')

plt.legend(loc='best')

plt.xlabel('Zeit in ns')
plt.ylabel('Spannung in V')

plt.savefig('Box25/Box25.pdf')

plt.show()
plt.close()


##Daten nach Latex
write('Box25/build/a.tex', make_SI(params[0], r'\volt', figures = 4))
write('Box25/build/b.tex', make_SI(params[1], r'', figures = 4))
write('Box25/build/c.tex', make_SI(params[2], r'\per\farad\per\ohm', figures = 4))
write('Box25/build/d.tex', make_SI(params[3], r'\nano\second', figures = 4))
write('Box25/build/e.tex', make_SI(params[4], r'\volt', figures = 4))

#kenngrößen des kabels berechnen (Z = 50 ohm)
#widerstand R
R = (50/params[1] -50)
write('Box25/build/R.tex', make_SI(R, r'\ohm', figures = 4))
C = 1/(params[2] * (50 + R) * 10 **9)
write('Box25/build/C.tex', make_SI(C*10**12, r'\pico\farad', figures = 4))

print(R)
print(C)





