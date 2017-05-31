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
x, y  = np.genfromtxt('Oszilloskop/Box28/F0052CH1.txt', unpack=True)

#den zu plottenden bereich heraussuchen (und nur jeden 4. wert nehmen):
x_plot = np.zeros(1900)
y_plot = np.zeros(1900)


#bereiche auswählen und in nenosekunden umrechen
for i in range(0, 1900):
	x_plot[i] = x[500+i]*10**9
	y_plot[i] = y[500+i]
	
plt.plot(x*10**9,y)
plt.show()
plt.close()


###Regression:

#Funktion definieren
def spannung(x, a, b, c, d, e):
    return 2*a*(1+b-b*np.exp(-c*(x-d))) + e
    
#x = np.linspace(0,800)
#plt.plot(x, spannung(x,-400, 0.379, 0.01, 0, 1500))
#plt.show()
#plt.close()



#Rechnung ohne Berücksichtigung eines Fehlers in y-Richtung
params, cov = curve_fit(spannung, x_plot, y_plot,(-400, 0.379, 0.01, 200, 1500))
print(params)
print(cov)

#plt.plot(x_plot, spannung(x_plot, 10, 1, 10**6, 10**(-7), -10), 'b-')
#plt.errorbar(x_vector, model(x_vector, params[0], params[1]), yerr=..., xerr=..., )
plt.plot(x*10**9, y, 'kx', label='Messwerte')
plt.plot(x_plot, spannung(x_plot, *params), 'r-', linewidth=2, label='Fit-Funktion')

plt.legend(loc='best')

plt.xlabel('Zeit in ns')
plt.ylabel('Spannung in V')

plt.savefig('Box28/Box28.pdf')
plt.show()
#print(x_plot)
plt.close()

##Daten nach Latex
write('Box28/build/a.tex', make_SI(params[0], r'\volt', figures = 4))
write('Box28/build/b.tex', make_SI(params[1], r'', figures = 4))
write('Box28/build/c.tex', make_SI(params[2], r'\ohm\per\henry', figures = 4))
write('Box28/build/d.tex', make_SI(params[3], r'\nano\second', figures = 4))
write('Box28/build/e.tex', make_SI(params[4], r'\volt', figures = 4))

#kenngrößen des kabels berechnen (Z = 50 ohm)
#widerstand R
R = (50/params[1] -50)
write('Box28/build/R.tex', make_SI(R, r'\ohm', figures = 4))
L = (R + 50) / (params[2]*10**9)
write('Box28/build/L.tex', make_SI(L*10**6, r'\micro\henry', figures = 4))



