import numpy as np
from uncertainties import ufloat
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp


L_flat, I_flat = np.genfromtxt('Daten/Daten_Stabilität_flat.txt', unpack = True)
L_curved, I_curved = np.genfromtxt('Daten/Daten_Stabilität_konfokal.txt', unpack = True)

# Umrechnen in SI-Einheiten
I_flat *= 10**(-9)
Ifmax = max(I_flat)
I_flat_norm = I_flat/Ifmax
I_curved *= 10**(-9)
Icmax = max(I_curved)
I_curved_norm = I_curved/Icmax
L_flat *= 10**(-2)
L_curved *= 10**(-2)

def g_curved(x, a, b, c):
    return a* x**2 + b*x +c
def g_flat(x, a,b):
    return a*x + b

parameter_curved, pcov_curved = curve_fit(g_curved, L_curved, I_curved_norm)
parameter_flat, pcov_flat = curve_fit(g_flat, L_flat, I_flat_norm)


x_curved = np.linspace(0.0,2.8,100)
plt.plot(x_curved, 1/(1.4)**2 * x_curved**2 - (2/1.4)*x_curved + 1, 'b', label = 'g(L)')
plt.plot(x_curved, g_curved(x_curved, parameter_curved[0], parameter_curved[1], parameter_curved[2]), 'r', label = 'Fit')
plt.plot(L_curved, I_curved_norm, 'kx', label = 'Masswerte')
#plt.axvline(x=0, color = 'b', linestyle = '--')
#plt.axvline(x=2.8, color = 'b', linestyle = '--')
#plt.axvline(x=0, color = 'r', linestyle = '--')
#plt.axvline(x=1.4, color = 'r', linestyle = '--')
plt.xlabel(r'$L \ / \mathrm{m}$')
plt.ylabel(r'$\mathrm{I}$')

plt.legend(loc='best')

plt.savefig('FitCurved.png')
plt.show()

x_flat = np.linspace(0.0, 1.4, 100)
plt.plot(x_flat, 1 - x_flat/1.400, 'b', label = 'g(L)')
plt.plot(x_flat, g_flat(x_flat, parameter_flat[0], parameter_flat[1]), 'r', label = 'Fit')
plt.plot(L_flat, I_flat_norm, 'kx', label = 'Messwerte')
plt.xlabel(r'$L \ / \mathrm{m}$')
plt.ylabel(r'$\mathrm{I}$')
plt.legend(loc='best')
plt.savefig('FitFlat.png')
plt.show()
