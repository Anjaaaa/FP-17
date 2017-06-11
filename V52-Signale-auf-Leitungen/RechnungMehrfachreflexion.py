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


t, U = np.genfromtxt("Oszilloskop/Mehrfachreflexion/F0054CH1.txt", unpack = True)

# Zeiteinheit: Microsekunden
t *= 10**6
# Spannungseinheit: kV
U *= 10**(-3)
# Vertical Offset (laut der CSV-Datei) ist 568
Offset = 0.568
U -= Offset
# Zeiten so verschieben, dass es bei 0 anfängt
t -= t[0]

# Grenzen für die Extraktionen
oben1 = -1.235 - Offset
oben2 = -0.555 - Offset
unten2 = -0.585 - Offset
oben3 = -0.430 - Offset
unten3 = -0.465 - Offset
unten4 = 0.110 - Offset

# Erstes Plateau extrahieren
t1 = []
P1 = []
for i in range(0,len(t)):
    if U[i] >= oben1:
        break
    if U[i]<oben1:
        P1.append(U[i])
        t1.append(t[i])

# Zweites Plateau extrahieren
t2 = []
P2 = []
for i in range(0,len(t)):
    if U[i]>unten2:
        if U[i]<oben2:
            P2.append(U[i])
            t2.append(t[i])

# Drittes Plateau extrahieren
t3 = []
P3 = []
for i in range(0,len(t)):
    if U[i]>unten3:
        if U[i]<oben3:
            P3.append(U[i])
            t3.append(t[i])

# Viertes Plateau extrahieren
t4 = []
P4 = []
for i in range(0,len(t)):
    if U[i]>unten4:
        P4.append(U[i])
        t4.append(t[i])


U0_nom = np.mean(P1)
U0_std = np.std(P1)/len(P1)
U0 = ufloat(U0_nom, U0_std)
U1_nom = np.mean(P2)
U1_std = np.std(P2)/len(P2)
U1 = ufloat(U1_nom, U1_std)
U2_nom = np.mean(P3)
U2_std = np.std(P3)/len(P3)
U2 = ufloat(U2_nom, U2_std)
U3_nom = np.mean(P4)
U3_std = np.std(P4)/len(P4)
U3 = ufloat(U3_nom, U3_std)

U0a = np.ones(10000)*U0_nom
U1a = np.ones(10000)*U1_nom
U2a = np.ones(10000)*U2_nom
U3a = np.ones(10000)*U3_nom

### Plot
x = np.linspace(0,0.5,10000)
plt.plot(t, U, 'k.', ms=1)
plt.plot(x, U0a, 'k', linestyle = 'dashed', linewidth = 0.5)
plt.plot(x, U1a, 'k', linestyle = 'dashed', linewidth = 0.5)
plt.plot(x, U2a, 'k', linestyle = 'dashed', linewidth = 0.5)
plt.plot(x, U3a, 'k', linestyle = 'dashed', linewidth = 0.5)

plt.plot(t1, P1, 'r.', ms=1)
plt.plot(t2, P2, 'b.', ms=1)
plt.plot(t3, P3, 'g.', ms=1)
plt.plot(t4, P4, 'y.', ms=1)

plt.ylabel(r'$U \ \mathrm{in} \ \mathrm{kHz}$')
plt.xlabel(r'$t \ \mathrm{in} \ \mathrm{ms}$')
plt.savefig('Plot.pdf')
plt.show()


#######################################################################################################################################
### Berechnung der Reflexionskonstanten
Delta1 = U1-U0
Delta2 = U2-U1
Delta3 = U3-U2
Gamma12 = -Delta1/U0
Gamma21 = 1 / (1 + Delta2**2 / (Delta3 *(-U0 - Delta1)))
GammaE = Delta3/Delta2 + Delta2/(-U0-Delta1)
print(Delta1)
print(Delta2)
print(Delta3)


#######################################################################################################################################
### Länge der Kabel ausrechenen
#Geschwindigkeit in Kupfer
v = 299792458 / np.sqrt(2.25)

# Zeit zwischen zwei Signalen (zwischen den Anfängen)
T1 = t2[0] - t1[0]
T2 = t3[0] - t2[0]
T3 = t4[0] - t3[0]

# Längen
L1 = T1*v/2 * 10**(-6) 
L21 = T2*v/2 * 10**(-6)
L22 = T3*v/2 * 10**(-6)
L2 = [L21,L22]
L2 = ufloat(np.mean(L2),np.std(L2)/np.sqrt(2))
print(L21)
print(L22)
### Werte in Latex-Dateien schreiben
write('Mehrfachreflexion/build/U0.tex', make_SI(U0, r'\kilo\volt', figures = 1))
write('Mehrfachreflexion/build/U1.tex', make_SI(U1, r'\kilo\volt', figures = 1))
write('Mehrfachreflexion/build/U2.tex', make_SI(U2, r'\kilo\volt', figures = 1))
write('Mehrfachreflexion/build/U3.tex', make_SI(U3, r'\kilo\volt', figures = 1))
write('Mehrfachreflexion/build/T1.tex', make_SI(T1, r'\micro\second', figures = 3))
write('Mehrfachreflexion/build/T2.tex', make_SI(T2, r'\micro\second', figures = 3))
write('Mehrfachreflexion/build/T3.tex', make_SI(T3, r'\micro\second', figures = 3))
write('Mehrfachreflexion/build/L1.tex', make_SI(L1, r'\meter', figures = 1))
write('Mehrfachreflexion/build/L2.tex', make_SI(L2, r'\meter', figures = 1))
write('Mehrfachreflexion/build/Gamma12.tex', make_SI(Gamma12, r'', figures = 1))
write('Mehrfachreflexion/build/Gamma21.tex', make_SI(Gamma21, r'', figures = 1))
write('Mehrfachreflexion/build/GammaE.tex', make_SI(GammaE, r'', figures = 1))

