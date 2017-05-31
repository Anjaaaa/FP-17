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

L = 50
fKurz, PKurz = np.genfromtxt("Oszilloskop/DaempfungKurz/DatenKurz.txt", unpack = True)
fLang, PLang = np.genfromtxt("Oszilloskop/DaempfungLang/DatenLang.txt", unpack = True)
# Einheiten: Hertz, dB
wKurz = fKurz*2*np.pi*10**(-6) # w in MHz
wLang = fLang*2*np.pi*10**(-6)


### Meine Lösung #################################################################################

# Berechne Omega0
w0 = np.zeros(2*len(wKurz))
for i in range(0,len(wKurz)):
    w0[i] = wKurz[i]/(2*i+1)
    w0[i+len(wKurz)] = wLang[i]/(2*i+1)
print(w0)
w0_nom = np.mean(w0)
w0_std = np.std(w0)/np.sqrt(len(w0))
w0 = ufloat(w0_nom, w0_std)
print('w0',w0)


# Theoriewert für P
def P(w):
    return 20*np.log10(w0_nom/w)

alpha = -(PLang-PKurz)/20/L/np.log10(np.exp(1))


### Plot
w = np.linspace(0.1,26,1000)
plt.plot(w, P(w), 'k-', label ='Theoretische Kurve ohne Dämpfung')
plt.plot(wKurz, PKurz, 'bx', label ='Messwerte kurzes Kabel')
plt.plot(wLang, PLang, 'rx', label ='Messwerte langes Kabel')
plt.xlim(0,26)
plt.ylim(-40,2.5)
plt.xlabel(r'$\omega \ \mathrm{in} \ \mathrm{MHz}$')
plt.ylabel(r'$P \ \mathrm{in} \ \mathrm{dB}$')

plt.legend(loc='best')
plt.savefig('Daempfung/build/PlotB.pdf')
plt.show()


### Werte in Latex-Dateien schreiben

write('Daempfung/build/tableB.tex', make_table([wKurz, -PKurz, wLang, -PLang, alpha*10**3],[3,2,3,2,2]))
write('Daempfung/build/fulltableB.tex', make_full_table(
    r'Frequenz $\omega$ und Betrag der Amplitude $P$ der Peaks in der FFT für das kurze und das lange Kabel, sowie mit \eqref{eq:DaempfungB} berechnete Dämpfung',
    'tab:DaempfungWerteB',
    'Daempfung/build/tableB.tex',
    [],
    [r'$\omega_\text{Kurz} \ \mathrm{in} \ \si{\mega\hertz}$',
    r'$|P_\text{Kurz}| \ \mathrm{in} \ \si{\deci\bel}$',
    r'$\omega_\text{Lang} \ \mathrm{in} \ \si{\mega\hertz}$',
    r'$|P_\text{Lang}| \ \mathrm{in} \ \si{\deci\bel}$',
    r'$\alpha \ \mathrm{in} \ \si{\per\kilo\meter}$']))
write('Daempfung/build/omega0', make_SI(w0,r'\mega\hertz', figures=2))
alpha_nom = np.mean(alpha)
alpha_std = np.std(alpha)/np.sqrt(len(alpha))
alpha = ufloat(alpha_nom, alpha_std)

write('Daempfung/build/alpha.tex', make_SI(alpha*10**3, r'\per\kilo\meter', figures = 2))
