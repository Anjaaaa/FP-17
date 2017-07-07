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


Lange50 = 10.8
Lange75 = 10.3

L50, R50, C50, f50 = np.genfromtxt("RLC_DirekteMessung/WerteRLC_50Ohm.txt", unpack = True)
L75, R75, f75, C75 = np.genfromtxt("RLC_DirekteMessung/WerteRLC_75Ohm.txt", unpack = True)
# Einheiten: microH, Ohm, pF, kHz
# Umrechnen (außer f)

L50 *= 10**(-6)
L75 *= 10**(-6)
C50 *= 10**(-12)
C75 *= 10**(-12)

# Theoriewerte
sigma = 56*10**6
mu = 4*np.pi*10**(-7)
eps = 2.25*8.854187*10**(-12)
D = 2.95*10**(-3)
d = 0.9*10**(-3)
Rconst = np.sqrt(mu/np.pi/sigma)*(1/d+1/D)
Lconst = mu/2/np.pi*np.log(D/d)
Cconst = 2*np.pi*eps/np.log(D/d)
Gconst = Rconst*Cconst/Lconst
def RT(f):
    return np.sqrt(f*10**3)*Rconst
def LT(f):
    return Lconst*f/f
def CT(f):
    return Cconst*f/f
def GT(f):
    return Gconst * np.sqrt(f*10**3)



### Plot
# R
print(L50)
#f = np.linspace(0.1,100.1,10)
plt.plot(f50, R50, 'gx', label ='Kabel 50$\Omega$')
plt.plot(f75, R75, 'y.', label ='Kabel 75$\Omega$')
plt.plot(f50, RT(f50)*Lange50, 'bx', label ='Theorie 50$\Omega$')#, linestyle = '-.')
plt.plot(f75, RT(f75)*Lange75, 'r.', label ='Theorie 75$\Omega$')#, linestyle = '--')

plt.xlabel(r'$f \ \mathrm{in} \ \mathrm{kHz}$')
plt.ylabel(r'$R \ \mathrm{in} \ \Omega$')
plt.xscale('log')

plt.legend(loc='best')
plt.savefig('RLC_DirekteMessung/build/PlotR.pdf')
plt.show()


# C
#f = np.linspace(0.1,100.1,1000)
plt.plot(f50, C50*10**9, 'gx', label ='Kabel 50$\Omega$')
plt.plot(f75, C75*10**9, 'y.', label ='Kabel 75$\Omega$')
plt.plot(f50, CT(f50)*Lange50*10**9, 'bx', label ='Theorie 50$\Omega$')
plt.plot(f75, CT(f75)*Lange75*10**9, 'r.', label ='Theorie 75$\Omega$')

plt.xlabel(r'$f \ \mathrm{in} \ \mathrm{kHz}$')
plt.ylabel(r'$C \ \mathrm{in} \ \mathrm{nF}$')
plt.xscale('log')

plt.legend(loc='best')
plt.savefig('RLC_DirekteMessung/build/PlotC.pdf')
plt.show()

# L
#f = np.linspace(0.1,100.1,1000)
plt.plot(f50, L50*10**6, 'gx', label ='Kabel 50$\Omega$')
plt.plot(f75, L75*10**6, 'y.', label ='Kabel 75$\Omega$')
plt.plot(f50, LT(f50)*Lange50*10**6, 'bx', label ='Theorie 50$\Omega$')
plt.plot(f75, LT(f75)*Lange75*10**6, 'r.', label ='Theorie 75$\Omega$')

plt.xlabel(r'$f \ \mathrm{in} \ \mathrm{kHz}$')
plt.ylabel(r'$L \ \mathrm{in} \ \mu\mathrm{F}$')
plt.xscale('log')

plt.legend(loc='best')
plt.savefig('RLC_DirekteMessung/build/PlotL.pdf')
plt.show()

# Einheiten Umrechnen microH, Ohm, pF, kHz

# G = RC/L
G50 = R50 * C50 / L50
G75 = R75 * C75 / L75

# G
#f = np.linspace(0.1,100.1,1000)
plt.plot(f50, G50*10**3, 'gx', label ='Kabel 50$\Omega$')
plt.plot(f75, G75*10**3, 'y.', label ='Kabel 75$\Omega$')
plt.plot(f50, GT(f50)*Lange50*10**3, 'bx', label ='Theorie 50$\Omega$')#, linestyle = 'dotted')
plt.plot(f75, GT(f75)*Lange75*10**3, 'r.', label ='Theorie 75$\Omega$')#, linestyle = 'dotted')

plt.xlabel(r'$f \ \mathrm{in} \ \mathrm{kHz}$')
plt.ylabel(r'$G \ \mathrm{in} \ \mathrm{mS}$')
plt.xscale('log')

plt.legend(loc='best')
plt.savefig('RLC_DirekteMessung/build/PlotG.pdf')
plt.show()




### Werte in Latex-Dateien schreiben

write('RLC_DirekteMessung/build/tableRLC50.tex', make_table([f50, R50, C50*10**12, L50*10**6, G50*10**3],[1,4,1,2,1]))
write('RLC_DirekteMessung/build/fulltableRLC50.tex', make_full_table(
    r'Beim Kurzschließen des $50\Omega$-Kables gemessene Werte für $R_{50},C_{50},L_{50}$ und daruas berechnete Werte für $G_{50}$ bei den jeweils eingestellten Frequenzen $f$',
    'tab:RLC50Werte',
    'RLC_DirekteMessung/build/tableRLC50.tex',
    [],
    [r'$f_{50} \ \mathrm{in} \ \si{\kilo\hertz}$',
    r'$R_{50} \ \mathrm{in} \ \si{\ohm}$',
    r'$C_{50} \ \mathrm{in} \ \si{\pico\farad}$',
    r'$L_{50} \ \mathrm{in} \ \si{\micro\henry}$',
    r'$G_{50} \ \mathrm{in} \ \si{\milli\siemens}$']))
write('RLC_DirekteMessung/build/tableRLC75.tex', make_table([f75, R75, C75*10**12, L75*10**6, G75*10**3],[0,2,1,2,1]))
write('RLC_DirekteMessung/build/fulltableRLC75.tex', make_full_table(
    r'Beim Kurzschließen des $75\Omega$-Kables gemessene Werte für $R_{75},C_{75},L_{75}$ und daraus berechnete Werte für $G_{75}$ bei den jeweils eingestellten Frequenzen $f$',
    'tab:RLC75Werte',
    'RLC_DirekteMessung/build/tableRLC75.tex',
    [],
    [r'$f_{75} \ \mathrm{in} \ \si{\kilo\hertz}$',
    r'$R_{75} \ \mathrm{in} \ \si{\ohm}$',
    r'$C_{75} \ \mathrm{in} \ \si{\pico\farad}$',
    r'$L_{75} \ \mathrm{in} \ \si{\micro\henry}$',
    r'$G_{75} \ \mathrm{in} \ \si{\milli\siemens}$']))

write('RLC_DirekteMessung/build/RTheorie.tex', make_SI(Rconst*10**6, r'\micro\ohm\per\meter', figures = 1))
write('RLC_DirekteMessung/build/CTheorie.tex', make_SI(Cconst*10**12, r'\pico\farad\per\meter', figures = 1))
write('RLC_DirekteMessung/build/LTheorie.tex', make_SI(Lconst*10**9, r'\nano\henry\per\meter', figures = 1))
write('RLC_DirekteMessung/build/GTheorie.tex', make_SI(Gconst*10**9, r'\nano\siemens\per\meter', figures = 1))

