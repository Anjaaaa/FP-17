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
x, y  = np.genfromtxt('Oszilloskop/GeschlossenesEnde/F0049CH1.txt', unpack=True)

#den zu plottenden bereich heraussuchen (und nur jeden 4. wert nehmen):
x_plot = np.zeros(400)
y_plot = np.zeros(400)


#bereiche auswählen und in nenosekunden umrechen
for i in range(0, 400):
	x_plot[i] = x[1600+i]*10**9
	y_plot[i] = y[1600+i]


###Regression:

#Funktion definieren
def spannung(x, a, b, c, d, e):
    return 2*a*(1+b-b*np.exp(-c*(x-d))) + e

#Rechnung ohne Berücksichtigung eines Fehlers in y-Richtung
params, cov = curve_fit(spannung, x_plot, y_plot, (-2.72, 0.379, 1, 500, 1.5))
#print(params)
#print(cov)


#plt.plot(x_plot, spannung(x_plot, 10, 1, 10**6, 10**(-7), -10), 'b-')
#plt.errorbar(x_vector, model(x_vector, params[0], params[1]), yerr=..., xerr=..., )
plt.plot(x_plot, y_plot, 'rx', label='Messwerte')
plt.plot(x_plot, spannung(x_plot, *params), label='Fit-Funktion')

plt.legend(loc='best')

plt.xlabel('Zeit in ns')
plt.ylabel('Spannung in V')

plt.savefig('Laplace/geschlossenes_ende.pdf')
#plt.show()
#print(x_plot)
plt.close()

##Daten nach Latex
write('Laplace/build/a_geschlossen.tex', make_SI(params[0], r'\volt', figures = 4))
write('Laplace/build/b_geschlossen.tex', make_SI(params[1], r'', figures = 4))
write('Laplace/build/c_geschlossen.tex', make_SI(params[2], r'\ohm\per\henry', figures = 4))
write('Laplace/build/d_geschlossen.tex', make_SI(params[3], r'\nano\second', figures = 4))
write('Laplace/build/e_geschlossen.tex', make_SI(params[4], r'\volt', figures = 4))

#kenngrößen des kabels berechnen (Z = 50 ohm)
#widerstand R
R_geschlossen = (50/params[1] -50)
write('Laplace/build/R_geschlossen.tex', make_SI(R_geschlossen, r'\ohm', figures = 4))
L_geschlossen = (R_geschlossen + 50) / (params[2]*10**9)
write('Laplace/build/L_geschlossen.tex', make_SI(L_geschlossen*10**6, r'\micro\henry', figures = 4))
#Geschwindigkeit in Kupfer
v = 299792458 / np.sqrt(2.25)
lange_geschlossen = v / (params[2] * 10**9)
write('Laplace/build/v.tex', make_SI(v, r'\meter\per\second', figures = 1))
write('Laplace/build/lange_geschlossen.tex', make_SI(lange_geschlossen, r'\meter', figures = 4))



#Offenes Ende
x, y  = np.genfromtxt('Oszilloskop/OffenesEnde/F0048CH1.txt', unpack=True)

#den zu plottenden bereich heraussuchen (und nur jeden 4. wert nehmen):
x_plot = np.zeros(400)
y_plot = np.zeros(400)


#bereich auswählen und in Megahertz umrechen
for i in range(0, 400):
	x_plot[i] = x[700+i]*10**9
	y_plot[i] = y[700+i]


###Regression:

#Funktion definieren
def spannung2(x, a, b, c, d, e):
    return 2*a*(1-b*np.exp(-c*(x-d))) + e

#Rechnung ohne Berücksichtigung eines Fehlers in y-Richtung
params, cov = curve_fit(spannung2, x_plot, y_plot, (4, 1, 0.01, -500, -10))
print(params)
print(cov)



#plt.errorbar(x_vector, model(x_vector, params[0], params[1]), yerr=..., xerr=..., )
plt.plot(x_plot, y_plot, 'rx', label = 'Messwerte')
plt.plot(x_plot, spannung2(x_plot, *params), 'b-', label = 'Fit-Funktion')

plt.legend(loc='best')

plt.xlabel('Zeit in ns')
plt.ylabel('Spannung in V')

plt.savefig('Laplace/offenes_ende.pdf')

plt.show()
plt.close()


##Daten nach Latex
write('Laplace/build/a_offen.tex', make_SI(params[0], r'\volt', figures = 4))
write('Laplace/build/b_offen.tex', make_SI(params[1], r'', figures = 4))
write('Laplace/build/c_offen.tex', make_SI(params[2], r'\per\farad\per\ohm', figures = 4))
write('Laplace/build/d_offen.tex', make_SI(params[3], r'\nano\second', figures = 4))
write('Laplace/build/e_offen.tex', make_SI(params[4], r'\volt', figures = 4))

#kenngrößen des kabels berechnen (Z = 50 ohm)
#widerstand R
R_offen = (50/params[1] -50)
write('Laplace/build/R_offen.tex', make_SI(R_offen, r'\ohm', figures = 4))
C_offen = 1/(params[2] * (50 + R_offen) * 10 **9)
write('Laplace/build/C_offen.tex', make_SI(C_offen*10**12, r'\pico\farad', figures = 4))

print(R_offen)
print(C_offen)

#Geschwindigkeit in Kupfer
v = 299792458 / np.sqrt(2.25)
lange_offen = v / (params[2] * 10**9)
print(lange_offen)
write('Laplace/build/lange_offen.tex', make_SI(lange_offen, r'\meter', figures = 4))



