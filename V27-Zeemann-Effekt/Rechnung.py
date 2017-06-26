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

Iup, Bup, Idown, Bdown = np.genfromtxt('Daten.txt', unpack = True)
red0, redSigma = np.genfromtxt('DatenRot.txt', unpack = True)
blue0, blueSigma, bluePi = np.genfromtxt('DatenBlau.txt', unpack = True)

# B in T
Bup *= 10**(-3)
Bdown *= 10**(-3)
bluePi *= 0.76 # sonst passt das Bild nicht zu den anderen

write('build/tableMesswerte.tex', make_table([Iup, Bup*1000, Idown, Bdown*1000],[1,0,1,0]))
write('build/fulltableMesswerte.tex', make_full_table(
    r'Strom und Magnetfeld beim Hoch- und Runterregeln des Magnetfelds',
    'tab:Messwerte',
    'build/tableMesswerte.tex',
    [],
    [r'$I_\mathrm{up} \ \mathrm{in} \ \si{\ampere}$',
    r'$B_\mathrm{up} \ \mathrm{in} \ \si{\milli\tesla}$',
    r'$I_\mathrm{down} \ \mathrm{in} \ \si{\ampere}$',
    r'$B_\mathrm{down} \ \mathrm{in} \ \si{\milli\tesla}$']))

write('build/tableFotosRed.tex', make_table([red0, redSigma],[0,0]))
write('build/fulltableFotosRed.tex', make_full_table(
    r'Abstände $\Delta s,\delta s$ in Pixel bei der roten Linie',
    'tab:WerteFotosRot',
    'build/tableFotosRed.tex',
    [],
    [r'$\Delta s_\mathrm{red}$',
    r'$\delta s_{\mathrm{red,}\sigma}$']))
write('build/tableFotosBlue.tex', make_table([blue0, blueSigma, bluePi],[0,0,0]))
write('build/fulltableFotosBlue.tex', make_full_table(
    r'Abstände $\Delta s,\delta s$ in Pixel bei der blauen Linie',
    'tab:WerteFotosBlau',
    'build/tableFotosBlue.tex',
    [],
    [r'$\Delta s_\mathrm{blue}$',
    r'$\delta s_{\mathrm{blue,}\sigma}$',
    r'$\delta s_{\mathrm{blue,}\pi}$']))

######################################################################################
### Konstanten
h = 6.626070040 * 10**(-34)     # Plancksches Wirkungsquantum
muB = 9.274009994 * 10**(-24)   # Bohrsches Magneton
c = 299792458
# Wellenlängen bei B = 0
waveLenRed = 643.8 * 10**(-9)
waveLenBlue = 480.0 * 10**(-9)
# Ausmaße Lummer-Gercke-Platte
d = 0.004
l = 0.120
# Brechungsindizes
nRed = 1.4567
nBlue = 1.4635
# Dispersionsgebiet
fRed = waveLenRed**2 /2/d * np.sqrt(1/(nRed**2-1))
fBlue = waveLenBlue**2 /2/d * np.sqrt(1/(nBlue**2-1))
# Auflösungsvermögen
aRed = l/waveLenRed * (nRed**2-1)
aBlue = l/waveLenBlue * (nBlue**2-1)
# Stromstärken bei der Aufspaltung
IRedSigma = 9
IBluePi = 15
IBlueSigma = 5



######################################################################################
### Eichung
# B,I in ein Array
Bges = np.concatenate((Bup,Bdown), axis=0)
Iges = np.concatenate((Iup,Idown), axis=0)
Bges = Bges[Bges > 0.001]  # Die "Nullen" rausnehmen.
Iges = Iges[Iges > 0]     # Alle Nullen rausnehmen.

# Ablese-Fehler
I_std = np.zeros(len(Iges))
I_std += 0.5

Iges = unp.uarray(Iges, I_std)

# Proportionalitätsfaktor
a = Bges/Iges
a = np.mean(a)

print(IRedSigma*a)
print(IBlueSigma*a)
print(IBluePi*a)


######################################################################################
### Ablesefehler Fotos
red_std = np.zeros(len(red0))
red_std +=20
blue_std = np.zeros(len(blue0))
blue_std += 20

red0 = unp.uarray(red0, red_std)
redSigma = unp.uarray(redSigma, red_std)
blue0 = unp.uarray(blue0, blue_std)
blueSigma = unp.uarray(blueSigma, blue_std)
bluePi = unp.uarray(bluePi, blue_std)



######################################################################################
### Berechnen der Landefaktoren
def g(ds, Ds, DispGebiet, lambda0, I):
    dLambda = 1/2 * ds / Ds * DispGebiet    # Wellenlängenverschiebung
    dE = h*c / lambda0**2 * dLambda         # Energieverschiebung
    g = dE / muB / (I*a)                    # Lande-Faktor
    return np.mean(g)

# Normaler Zeemann-Effekt: dE = dm * g * muB * B (dm = +1,0,-1)
gRedSigma = g(redSigma, red0, fRed, waveLenRed, IRedSigma)
# Anomaler Zeemann-Effekt: dE = (m1*g1 - m2*g2) * muB * B = g * muB * B
gBlueSigma = g(blueSigma, blue0, fBlue, waveLenBlue, IBlueSigma)
gBluePi = g(bluePi, blue0, fBlue, waveLenBlue, IBluePi)



######################################################################################
### Werte in Latex-Dateien schreiben
write('build/gRedSigma.tex', make_SI(gRedSigma, r'', figures = 1))
write('build/gBlueSigma.tex', make_SI(gBlueSigma, r'', figures = 1))
write('build/gBluePi.tex', make_SI(gBluePi, r'', figures = 1))

write('build/Steigung.tex', make_SI(a, r'\tesla\per\ampere', figures = 2))

#write('build/I1.tex', make_SI(I1, r'', figures = 1))
#write('build/I2.tex', make_SI(I2, r'', figures = 1))

#write('build/Bvert.tex', make_SI(Bvert*10**6, r'\micro\tesla', figures = 1))
#write('build/BErdeA.tex', make_SI(BErdeA*10**6, r'\micro\tesla', figures = 1))
#write('build/BErdeB.tex', make_SI(BErdeB*10**6, r'\micro\tesla', figures = 1))

#write('build/T1.tex', make_SI(T1, r'', figures = 1))
#write('build/T2.tex', make_SI(T2, r'', figures = 1))
#write('build/Ratio.tex', make_SI(Ratio, r'', figures = 1))

#write('build/quadrat1.tex', make_SI(verhaeltnis1*10**27, r'', exp='e-27',figures = 1))
#write('build/quadrat2.tex', make_SI(verhaeltnis2*10**27, r'', exp='e-27', figures = 1))
