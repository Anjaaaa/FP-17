import numpy as np
from uncertainties import ufloat
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp
from table import (
        make_table,
        make_full_table,
        make_SI,
        write)

f, sweep1, hor1, sweep2, hor2 = np.genfromtxt('Data.txt', unpack = True)
vert = 1.45
write('build/tableMesswerte.tex', make_table([f, sweep1, hor1, sweep2, hor2],[0,2,2,2,2]))
write('build/fulltableMesswerte.tex', make_full_table(
    r'Position der ersten und zweiten Resonanzstelle für verschiedene Frequenzen ',
    'tab:Messwerte',
    'build/tableMesswerte.tex',
    [],
    [r'$f \ \mathrm{in} \ \si{\kilo\hertz}$',
    r'Sweep 1',
    r'Horizontal 1',
    r'Sweep 2',
    r'Horizontal 2']))


### Konstanten
mu0 = 4*np.pi*10**(-7)
h = 6.626070040 * 10**(-34)
me = 9.10938356 * 10**(-31)
muB = 9.274009994 * 10**(-24)
Rsweep = 16.39 * 10**(-2)
Nsweep = 11
Rhor = 15.79 * 10**(-2)
Nhor = 154
Rvert = 11.735 * 10**(-2)
Nvert = 20

######################################################################################
### Umrechnen in SI-Einheiten
f *= 1000
# Der Ablesefehler an der Schraube ist 0.01, der Ablesefehler am Oszilloskop ist 0.20.
sweep_std = np.zeros(10)
sweep_std += 0.20
sweep1 = unp.uarray(sweep1, sweep_std)
sweep2 = unp.uarray(sweep2, sweep_std)
vert = unp.uarray(vert, 0.01)
hor_std = np.zeros(10)
hor_std += 0.01
hor1 = unp.uarray(hor1, hor_std)
hor2 = unp.uarray(hor2, hor_std)

# sweep, vert: Maximal 1A, d.h. ein Wert von 5.43 entspricht 0.543A
# hor: Maximal 3A, d.h. ein Wert von 5.43 entspricht 0.3*5.43A
sweep1 *= 0.1
sweep2 *= 0.1
vert *= 0.1
hor1 *= 0.3
hor2 *= 0.3

######################################################################################
### Umrechnen der Stromstärken in Magnetfelder
def B(I,R,N):
    return mu0 * 8/np.sqrt(125) * I*N/R
Bsweep1 = B(sweep1,Rsweep,Nsweep)
Bsweep2 = B(sweep2,Rsweep,Nsweep)
Bhor1 = B(hor1,Rhor,Nhor)
Bhor2 = B(hor2,Rhor,Nhor)
Bvert = B(vert,Rvert,Nvert)
### Addieren der horizontelen Magnetfelder
B1 = Bsweep1 + Bhor1
B2 = Bsweep2 + Bhor2
### Umrechnen zum besseren Fitten und Plotten
B1_nom = unp.nominal_values(B1)
B1_std = unp.std_devs(B1)
B2_nom = unp.nominal_values(B2)
B2_std = unp.std_devs(B2)

######################################################################################
### Fit
def B(f,m,t):
    return m*f + t
val1, std1 = curve_fit(B, f, B1_nom, sigma = B1_std)
val2, std2 = curve_fit(B, f, B2_nom, sigma = B2_std)


### Plot
nu = np.linspace(0,1.1*10**6,1000)
plt.plot(nu*10**-3, B(nu,*val1)*10**3, 'deepskyblue', label = 'Fit 1')
plt.plot(nu*10**-3, B(nu,*val2)*10**3, 'lime', label = 'Fit 2')
plt.plot(f*10**-3, B1_nom*10**3, 'b.', label ='Messwerte 1')
plt.plot(f*10**-3, B2_nom*10**3, 'g.', label = 'Messwerte 2')
plt.errorbar(f*10**-3, B1_nom*10**3, yerr = B1_std*10**3, capsize=0.8, elinewidth = 0.8, color = 'b', ls = 'none')
plt.errorbar(f*10**-3, B2_nom*10**3, yerr = B2_std*10**3, capsize=0.8, elinewidth = 0.8, color = 'g', ls = 'none')

plt.xlim(0,1.1*10**3)
plt.xlabel(r'$f \ \mathrm{in} \ \mathrm{kHz}$')
plt.ylabel(r'$B \ \mathrm{in} \ \mathrm{mT}$')

plt.legend(loc='best')
plt.savefig('Fit.pdf')
#plt.show()


#####################################################################################
### Landefaktor (~Steigung)
m1 = ufloat(val1[0], np.sqrt(std1[0,0]))
m2 = ufloat(val2[0], np.sqrt(std2[0,0]))
g1 = h/muB/m1
g2 = h/muB/m2

### Horizontal-Komponente des Magentfelds (= Achsenabschnitt)
BhorErde1 = ufloat(val1[1], np.sqrt(std1[1,1]))
BhorErde2 = ufloat(val2[1], np.sqrt(std2[1,1]))
# Mittelwert mit Fehler der Fehlerfortpflanzung
BEA = (BhorErde1+BhorErde2)/2
# Mittelwert mit Fehler des Mittelwerts
BEB = np.array(val1[1], val2[1])
mean = np.mean(BEB)
std = np.std(BEB)
BEB = ufloat(mean, std/np.sqrt(2))

### Erdmagnetfeld
BErdeA = unp.sqrt(Bvert**2 + BEA**2)
BErdeB = unp.sqrt(Bvert**2 + BEB**2)

### Kernspin
# Nur Spin bei J, gJ, da Rubidium Alkalimetall ist.
J = 1/2
gJ = 2.002319304
b1 = J*(2-gJ/g1)+1
b2 = J*(2-gJ/g2)+1
c1 = J*(J+1)*(1-gJ/g1)
c2 = J*(J+1)*(1-gJ/g2)
I1 = -b1/2 + unp.sqrt(b1**2/4 - c1)
I2 = -b2/2 + unp.sqrt(b2**2/4 - c2)

### Isotopenverhältnis
Tmax = ufloat(3.47, 0.25)
T1 = ufloat(2.69, 0.25)
T1 = T1/Tmax
T2 = ufloat(1.80 ,0.25)
T2 = T2/Tmax
Ratio = T1/T2

### quadtrtischer zeemann-effekt
#Energiedifferenzen sind angegeben in der anleitung:
E1 = 4.53E-24 #rubidium-87
E2 = 2.01E-24 #rubidium-85

B = 0.5E-3 #für die abschätzung wähle ich einen wert für das B-Feld, der größer ist als alle gemessenen resonanzen

E1_quadrat = g1*g1*muB*muB*B*B*(1-2*(3/2))
E2_quadrat = g2*g2*muB*muB*B*B*(1-2*(5/2))

#anteil der quadtratischen terms an der energielücke:

verhaeltnis1 = E1_quadrat / (g1*muB*B + E1_quadrat)
verhaeltnis2 = E2_quadrat / (g2*muB*B + E2_quadrat)

print(verhaeltnis1)
print(verhaeltnis2)


###################################################################################
### Werte in Latex-Dateien schreiben
write('build/tableRegression.tex', make_table([f*10**-3, B1_nom*10**3, B2_nom*10**3],[0,3,3]))
write('build/fulltableRegression.tex', make_full_table(
    r'Bei der Regression verwendete Werte, die Unsicherheit beträgt für alle $B_1, B_2$ \SI{2.9}{\micro\tesla}',
    'tab:Regression',
    'build/tableRegression.tex',
    [],
    [r'$f \ \mathrm{in} \ \si{\kilo\hertz}$',
    r'$B_1 \ \mathrm{in} \ \si{\milli\tesla}$',
    r'$B_2 \ \mathrm{in} \ \si{\milli\tesla}$']))

write('build/Lande1.tex', make_SI(g1, r'', figures = 1))
write('build/Lande2.tex', make_SI(g2, r'', figures = 1))

write('build/Bhor1.tex', make_SI(BhorErde1*10**6, r'\micro\tesla', figures = 1))
write('build/Bhor2.tex', make_SI(BhorErde2*10**6, r'\micro\tesla', figures = 1))

write('build/I1.tex', make_SI(I1, r'', figures = 1))
write('build/I2.tex', make_SI(I2, r'', figures = 1))

write('build/Bvert.tex', make_SI(Bvert*10**6, r'\micro\tesla', figures = 1))
write('build/BErdeA.tex', make_SI(BErdeA*10**6, r'\micro\tesla', figures = 1))
write('build/BErdeB.tex', make_SI(BErdeB*10**6, r'\micro\tesla', figures = 1))

write('build/T1.tex', make_SI(T1, r'', figures = 1))
write('build/T2.tex', make_SI(T2, r'', figures = 1))
write('build/Ratio.tex', make_SI(Ratio, r'', figures = 1))

write('build/quadrat1.tex', make_SI(verhaeltnis1*10**27, r'', exp='e-27',figures = 1))
write('build/quadrat2.tex', make_SI(verhaeltnis2*10**27, r'', exp='e-27', figures = 1))
