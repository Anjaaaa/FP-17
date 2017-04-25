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
g_flat = 1 - L_flat/1.400
g_curved = 1/(1.4)**2 * L_curved**2 - (2/1.4)*L_curved + 1


#plt.plot(L_flat, g_flat, 'r.')
#plt.plot(L_curved, g_curved, 'b.')
#x_flat = np.linspace(0.0, 1.4, 100)
#x_curved = np.linspace(0.0,2.8,100)
#plt.plot(x_flat, 1 - x_flat/1.400, 'r')
#plt.plot(x_curved, 1/(1.4)**2 * x_curved**2 - (2/1.4)*x_curved + 1, 'b')

plt.plot(L_flat, I_flat_norm, 'r.')
plt.plot(L_curved, I_curved_norm, 'b.')
#plt.axvline(x=0, color = 'b', linestyle = '--')
#plt.axvline(x=2.8, color = 'b', linestyle = '--')
#plt.axvline(x=0, color = 'r', linestyle = '--')
#plt.axvline(x=1.4, color = 'r', linestyle = '--')




plt.show()

