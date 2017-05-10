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

Max1 = unp.uarray(max1, unc1) * 10**(-3)
Max2 = unp.uarray(max2, unc2) * 10**(-3)
Max = (Max2-Max1)/2

nuE *= 10**6

### Umrechnung in B
B = 8/np.sqrt(125) * 4*np.pi * 4*np.pi * 10**(-7) * 156/0.1 * Max  # Ergebnis in Tesla

### Erdmagnetfeld
Erde = np.mean(B)
print(Erde)

### Ausgleichsrechnung
BNom = unp.nominal_values(B)
BDev = unp.std_devs(B)

def Bfunc(nu, g): # Bfunc = nu / g / mu0 * h
    return nu / g / (9.274051 * 10**(-24)) * 6.626070040*10**(-34) 

gFit, gErr = curve_fit(Bfunc, nuE, BNom, p0 = [1], sigma = BDev)


print(gFit[0], gErr[0,0])
print('BNom: ', BNom)
print('Bfunc: ',Bfunc(nuE,1))


# Plot
x = np.linspace(10*10**6,30*10**6,100)
plt.plot(x, Bfunc(x, 1), 'b', label ='Theorie')
plt.plot(x, Bfunc(x, gFit[0]), 'r', label = 'Fit')
plt.plot(nuE, BNom, 'kx', label = 'Messwerte')
plt.xlim(10*10**6,30*10**6)
#plt.xlabel(r'$$')
#plt.ylabel(r'$$')

plt.legend(loc='best')

plt.savefig('FitCurved.pdf')
plt.show()
