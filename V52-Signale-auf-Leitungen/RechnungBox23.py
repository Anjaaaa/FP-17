import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat
import matplotlib.pyplot as plt

from table import (
        make_table,
        make_full_table,
        make_SI,
        write)

#Geschlossenes Ende:
x, y  = np.genfromtxt('Oszilloskop/Box23/F0050CH1.txt', unpack=True)

#den zu plottenden bereich heraussuchen (und nur jeden 4. wert nehmen):
x_plot = np.zeros(900)
y_plot = np.zeros(900)


#bereiche auswählen und in nenosekunden umrechen
for i in range(0, 900):
	x_plot[i] = x[1517+i]*10**9
	y_plot[i] = y[1517+i]
	
plt.plot(x*10**9,y)
plt.show()
plt.close()


###Regression:

#Funktion definieren
def spannung(x, a, b, c, d, e):
    return 2*a*(1+b-b*np.exp(-c*(x-d))) + e
    
    



#Rechnung ohne Berücksichtigung eines Fehlers in y-Richtung
params, cov = curve_fit(spannung, x_plot, y_plot, (-15, 0.379, 0.01, 100, 40))
print(params)
print(cov)

#plt.plot(x_plot, spannung(x_plot, 10, 1, 10**6, 10**(-7), -10), 'b-')
#plt.errorbar(x_vector, model(x_vector, params[0], params[1]), yerr=..., xerr=..., )
plt.plot(x*10**9, y, 'kx', label='Messwerte')
plt.plot(x_plot, spannung(x_plot, *params), 'r-', linewidth=2, label='Fit-Funktion')

plt.legend(loc='best')

plt.xlabel('Zeit in ns')
plt.ylabel('Spannung in V')

plt.savefig('Box23/Box23.pdf')
plt.show()
#print(x_plot)
plt.close()

##Daten nach Latex
write('Box23/build/a.tex', make_SI(params[0], r'\volt', figures = 4))
write('Box23/build/b.tex', make_SI(params[1], r'', figures = 4))
write('Box23/build/c.tex', make_SI(params[2], r'\ohm\per\henry', figures = 4))
write('Box23/build/d.tex', make_SI(params[3], r'\nano\second', figures = 4))
write('Box23/build/e.tex', make_SI(params[4], r'\volt', figures = 4))

#kenngrößen des kabels berechnen (Z = 50 ohm)
#widerstand R
R = (50/params[1] -50)
write('Box23/build/R.tex', make_SI(R, r'\ohm', figures = 4))
L = (R + 50) / (params[2]*10**9)
write('Box23/build/L.tex', make_SI(L*10**6, r'\micro\henry', figures = 4))



