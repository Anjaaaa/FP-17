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


L50, R50, C50, f50 = np.genfromtxt("WerteRLC_50Ohm.txt", unpack = True)
L75, R75, f75, C75 = np.genfromtxt("WerteRLC_75Ohm.txt", unpack = True)
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
print(Rconst)
print(Cconst)
print(Lconst)

def RT(f):
    return np.sqrt(f*10**3)*Rconst
def LT(f):
    return Lconst*f/f
def CT(f):
    return Cconst*f/f
def GT(f):
    return Rconst*Cconst/Lconst * np.sqrt(f*10**3)
### Plot
# R
f = np.linspace(0.1,100.1,1000)
plt.plot(f50, R50, 'b.', label ='Kabel 50$\Omega$')
plt.plot(f75, R75, 'r.', label ='Kabel 75$\Omega$')
plt.plot(f, RT(f)*10, 'k', label ='Theorie')

#plt.plot(, BNom*10**3, 'k.', label = 'Messwerte mit Ungenauigkeit')
#plt.errorbar(nuE, BNom*10**3, yerr=BDev*10**3, fmt = 'x', color = 'k')
#plt.xlim(0,33)
#plt.ylim(0,Bfunc(33, 2.002319)*10**3)
plt.xlabel(r'$f \ \mathrm{in} \ \mathrm{kHz}$')
plt.ylabel(r'$R \ \mathrm{in} \ \Omega$')
plt.xscale('log')

plt.legend(loc='best')
plt.savefig('PlotR.pdf')
plt.show()

# C
f = np.linspace(0.1,100.1,1000)
plt.plot(f50, C50*10**9, 'b.', label ='Kabel 50$\Omega$')
plt.plot(f75, C75*10**9, 'r.', label ='Kabel 75$\Omega$')
plt.plot(f, CT(f)*10*10**9, 'k', label ='Theorie')

#plt.plot(, BNom*10**3, 'k.', label = 'Messwerte mit Ungenauigkeit')
#plt.errorbar(nuE, BNom*10**3, yerr=BDev*10**3, fmt = 'x', color = 'k')
#plt.xlim(0,33)
#plt.ylim(0,Bfunc(33, 2.002319)*10**3)
plt.xlabel(r'$f \ \mathrm{in} \ \mathrm{kHz}$')
plt.ylabel(r'$C \ \mathrm{in} \ \mathrm{nF}$')
plt.xscale('log')

plt.legend(loc='best')
plt.savefig('PlotC.pdf')
plt.show()

# L
f = np.linspace(0.1,100.1,1000)
plt.plot(f50, L50*10**6, 'b.', label ='Kabel 50$\Omega$')
plt.plot(f75, L75*10**6, 'r.', label ='Kabel 75$\Omega$')
plt.plot(f, LT(f)*10*10**6, 'k', label ='Theorie')

#plt.plot(, BNom*10**3, 'k.', label = 'Messwerte mit Ungenauigkeit')
#plt.errorbar(nuE, BNom*10**3, yerr=BDev*10**3, fmt = 'x', color = 'k')
#plt.xlim(0,33)
#plt.ylim(0,Bfunc(33, 2.002319)*10**3)
plt.xlabel(r'$f \ \mathrm{in} \ \mathrm{kHz}$')
plt.ylabel(r'$L \ \mathrm{in} \ \mu\mathrm{F}$')
plt.xscale('log')

plt.legend(loc='best')
plt.savefig('PlotL.pdf')
plt.show()

# Einheiten Umrechnen microH, Ohm, pF, kHz

# G = RC/L
G50 = R50 * C50 * 10**12 / L50 * 10**(-6)
G75 = R75 * C75 * 10**12 / L75 * 10**(-6)

# G
f = np.linspace(0.1,100.1,1000)
plt.plot(f50, G50, 'b.', label ='Kabel 50$\Omega$')
plt.plot(f75, G75, 'r.', label ='Kabel 75$\Omega$')
plt.plot(f, GT(f)*10, 'k', label ='Theorie')

#plt.plot(, BNom*10**3, 'k.', label = 'Messwerte mit Ungenauigkeit')
#plt.errorbar(nuE, BNom*10**3, yerr=BDev*10**3, fmt = 'x', color = 'k')
#plt.xlim(0,33)
#plt.ylim(0,Bfunc(33, 2.002319)*10**3)
plt.xlabel(r'$f \ \mathrm{in} \ \mathrm{kHz}$')
plt.ylabel(r'$G \ \mathrm{in} \ \Omega^{-1}$')
plt.xscale('log')

plt.legend(loc='best')
plt.savefig('PlotG.pdf')
plt.show()


Max2 = unp.uarray(max2, unc2) * 10**(-3)

### Ausgleichsrechnung
B = (B1+B2)/2               # Bereinigte Flussdichte (ohne Erdmagnetfeld)
BNom = unp.nominal_values(B)
BDev = unp.std_devs(B)

def Bfunc(nu, g): # Bfunc = nu / g / mu0 * h
    return nu*10**6 / g / (9.274051 * 10**(-24)) * 6.626070040*10**(-34) 

gFit, gErr = curve_fit(Bfunc, nuE, BNom, p0 = [1], sigma = BDev)


print('Lande-Faktor: ', gFit[0], '+-', gErr[0,0])
print('Obere Grenze Toleranzbereich:', gFit+gErr)
print('Lande-Faktor (Literatur): ', 2.002319)

### Plot
x = np.linspace(0,33,3)
plt.plot(x, Bfunc(x, 2.002319)*10**3, 'b', label ='Literatur')
plt.plot(x, Bfunc(x, gFit[0])*10**3, 'r', label = 'Fit')
plt.plot(nuE, BNom*10**3, 'k.', label = 'Messwerte mit Ungenauigkeit')
plt.errorbar(nuE, BNom*10**3, yerr=BDev*10**3, fmt = 'x', color = 'k')
plt.xlim(0,33)
#plt.ylim(0,Bfunc(33, 2.002319)*10**3)
plt.xlabel(r'$\nu_e \ \mathrm{in} \ \mathrm{MHz}$')
plt.ylabel(r'$B \ \mathrm{in} \ \mathrm{mT}$')

### Unnötiges Einzeichnen des Toleranzbereichs
#gMin = gFit[0]-gErr[0,0]
#gMax = gFit[0]+gErr[0,0]
#plt.fill_between(x, Bfunc(x,gMin)*10**3, Bfunc(x,gMax)*10**3, color = 'red', alpha = 0.25, label = 'Toleranzbereich')

plt.legend(loc='best')
plt.savefig('Fit.pdf')
plt.show()



### Werte in Latex-Dateien schreiben

write('build/tableMesswerte.tex', make_table([nuE, Max1*10**3, Max2*10**3, scale],[3,1,1,1]))
write('build/fulltableMesswerte.tex', make_full_table(
    r'Stromstärken $I_1,I_2$ beim Auftreten des Maximums für verschiedene Anregungsfrequenzen $\nu_e$ mit dem jeweiligen Skalierungsfaktor',
    'tab:Werte',
    'build/tableMesswerte.tex',
    [1,2,3],
    [r'$\nu_e \ \mathrm{in} \ \si{\mega\hertz}$',
    r'$I_1 \ \mathrm{in} \ \si{\milli\ampere}$',
    r'$I_2 \ \mathrm{in} \ \si{\milli\ampere}$',
    r'Skala in \si{\milli\ampere\per\centi\meter}']))

write('build/tableRegression.tex', make_table([nuE, B*10**3, BErde*10**3],[3,1,1]))
write('build/fulltableRegression.tex', make_full_table(
    r'Frequenzen $\nu_e$ und dazugehörige erdmagnetfeld-bereinigte Flussdichten $B$ der Helmholtz-Spulen, sowie das berechnete Erdmagnetfeld $B_\text{Erde}$',
    'tab:BFeld',
    'build/tableRegression.tex',
    [1,2],
    [r'$\nu_e \ \mathrm{in} \ \si{\mega\hertz}$',
    r'$B \ \mathrm{in} \ \si{\milli\tesla}$',
    r'$B_\text{Erde} \ \mathrm{in} \ \si{\milli\tesla}$']))

g = ufloat(gFit, np.sqrt(gErr))
write('build/Erdmagnetfeld.tex', make_SI(Erde*10**3, r'\milli\tesla', figures = 1))
write('build/Landefaktor.tex', make_SI(g, r'', figures = 1))
