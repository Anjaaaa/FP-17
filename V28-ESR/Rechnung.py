import numpy as np
from uncertainties import ufloat
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp

from table import (
        make_table,
        make_full_table,
        make_SI,
        write)


nuOsz, nuE, max1, unc1, max2, unc2 = np.genfromtxt("Daten.txt", unpack = True)
# Frequenzen in MHz, Maxima in mA
# nuE bleiben auch die ganze Zeit in MHz, die 10**6 werden in den Rechnung hinzugefügt
Max1 = unp.uarray(max1, unc1) * 10**(-3)
Max2 = unp.uarray(max2, unc2) * 10**(-3)
Max = (Max2-Max1)/2


### Umrechnung in B
B = 8/np.sqrt(125) * 4*np.pi * 4*np.pi * 10**(-7) * 156/0.1 * Max  # Ergebnis in Tesla

### Erdmagnetfeld
Erde = np.mean(B)
print('Erde: ', Erde)

### Ausgleichsrechnung
BNom = unp.nominal_values(B)
BDev = unp.std_devs(B)

def Bfunc(nu, g): # Bfunc = nu / g / mu0 * h
    return nu*10**6 / g / (9.274051 * 10**(-24)) * 6.626070040*10**(-34) 

gFit, gErr = curve_fit(Bfunc, nuE, BNom, p0 = [1], sigma = BDev)


print('Lande-Faktor: ', gFit[0], '+-', gErr[0,0])
print('Untere Grenze Toleranzbereich:', gFit-gErr)
print('Lande-Faktor (Literatur): ', 2.002319)

# Plot
x = np.linspace(0,33,3)
plt.plot(x, Bfunc(x, 2.002319)*10**3, 'b', label ='Theorie')
plt.plot(x, Bfunc(x, gFit[0])*10**3, 'r', label = 'Fit')
plt.plot(nuE, BNom*10**3, 'kx', label = 'Messwerte')
plt.errorbar(nuE, BNom*10**3, yerr=BDev*10**3, fmt = 'x', color = 'k')
plt.xlim(0,33)
#plt.ylim(0,Bfunc(33, 2.002319)*10**3)
plt.xlabel(r'$\nu \ \mathrm{in} \ \mathrm{MHz}$')
plt.ylabel(r'$B \ \mathrm{in} \ \mathrm{mT}$')


### Unnötiges Einzeichnen des Toleranzbereichs
gMin = gFit[0]-gErr[0,0]
gMax = gFit[0]+gErr[0,0]

plt.fill_between(x, Bfunc(x,gMin)*10**3, Bfunc(x,gMax)*10**3, color = 'red', alpha = 0.25, label = 'Toleranzbereich')


plt.legend(loc='best')

plt.savefig('Fit.pdf')
plt.show()



### Werte in Latex-Dateien schreiben

write('build/tableMesswerte.tex', make_table([nuE, Max1*10**3, Max2*10**3],[3,1,1]))
write('build/fulltableMesswerte.tex', make_full_table(
    r'Stromstärke $I_1,I_2$ beim Auftreten des Maximums für verschiedene Anregungsfrequenzen $\nu$',
    'tab:Werte',
    'build/tableMesswerte.tex',
    [1,2],
    [r'$\nu \ \mathrm{in} \ \si{\mega\hertz}$',
    r'$I_1 \ \mathrm{in} \ \si{\milli\ampere}$',
    r'$I_2 \ \mathrm{in} \ \si{\milli\ampere}$']))

write('build/tableRegression.tex', make_table([nuE, B*10**3],[3,1]))
write('build/fulltableRegression.tex', make_full_table(
    r'Bei der Regression verwendete Werte',
    'tab:Regression',
    'build/tableRegression.tex',
    [1],
    [r'$\nu \ \mathrm{in} \ \si{\mega\hertz}$',
    r'$B \ \mathrm{in} \ \si{\milli\tesla}$']))

g = ufloat(gFit, gErr)
write('build/Erdmagnetfeld.tex', make_SI(Erde*10**3, r'\milli\tesla', figures = 1))
write('build/Landefaktor.tex', make_SI(g, r'', figures = 2))
