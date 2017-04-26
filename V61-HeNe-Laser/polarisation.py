import numpy as np
import uncertainties
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize_scalar
from sympy import *
from table import (
        make_table,
        make_full_table,
        make_SI,
        write)



phi, I = np.genfromtxt('Daten/Daten_Polarisation.txt', unpack = True)
phi *= 2*np.pi/360
I *= 10**(-6)

write('build/tablePolarisation.tex', make_table([phi, I*10**6],[2,0]))
write('build/fulltablePolarisation.tex', make_full_table(
    r'Intensität in Abhängigkeit des Winkels des Polarisators',
    'tab:Polarisation',
    'build/tablePolarisation.tex',
    [],
    [r'$\varphi$',
    r'$I \ \mathrm{in} \ \si{\micro\ampere}$']))

def func(x, a,b,c):
  return a*np.sin(b*x+c)**2

a_0 = 0.0001
b_0 = 1
c_0 = 0.4
parameter, pcov = curve_fit(func, phi, I, p0=(a_0, b_0, c_0))
a = ufloat(parameter[0], np.sqrt(pcov[0,0]))
b = ufloat(parameter[1], np.sqrt(pcov[1,1]))
c = ufloat(parameter[2], np.sqrt(pcov[2,2]))
write('build/PolAmplitude.tex', make_SI(a*10**6, r'\micro\ampere', figures=1))
write('build/PolFrequenz.tex', make_SI(b, r'', figures = 1))
write('build/PolOffset.tex', make_SI(c/np.pi, r'\pi',  figures = 1))
print(parameter[0])
print(parameter[1])
print(parameter[2])
x = np.arange(0, 2*np.pi, 0.01 )
plt.plot(x, 10**6*func(x,parameter[0], parameter[1], parameter[2]), color = 'r', label = 'Fit')
plt.plot(phi, 10**6*I, 'kx', label='Messwerte')
plt.xlim(0, 2*np.pi)
plt.xlabel(r'$\mathrm{\varphi}$')
plt.ylabel(r'$I \ \mathrm{in} \ \mathrm{\mu}$A')
plt.legend(loc='best')
plt.savefig('Fit_Polarisation.png')
plt.show()

# Maximum der Funktion finden
x = np.linspace(0, np.pi, 10000)
y = func(parameter[0], parameter[1], parameter[2],x)
xmax = max(y)
print(xmax)
write('build/PolMax.tex', make_SI(xmax/np.pi, r'', '\pi', figures = 1))
