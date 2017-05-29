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
alpha = -20/L*(PLang-PKurz)
print('alpha: ',ufloat(np.mean(alpha), np.std(alpha)/np.sqrt(len(alpha))))


def f(w,a,b,c):
    return a*np.exp(b*w)+c
def g(w,a,b,c):
    return a/(w+b) + c

paramfKurz, sigmafKurz = curve_fit(f, wKurz, PKurz, [1,-1,-50])
paramgKurz, sigmagKurz = curve_fit(g, wKurz, PKurz, [10,0,-50])
paramfLang, sigmafLang = curve_fit(f, wLang, PLang, [1,-1,-50])
paramgLang, sigmagLang = curve_fit(g, wLang, PLang, [10,0,-50])

### Güte des Fits
resfKurz = PKurz- f(wKurz, *paramfKurz)
ss_resfKurz = np.sum(resfKurz**2)
ss_totKurz = np.sum((PKurz-np.mean(PKurz))**2)
r_squaredfKurz = 1 - (ss_resfKurz / ss_totKurz)
print('Gute fKurz: ',r_squaredfKurz)
resgKurz = PKurz- g(wKurz, *paramgKurz)
ss_resgKurz = np.sum(resgKurz**2)
r_squaredgKurz = 1 - (ss_resgKurz / ss_totKurz)
print('Gute gKurz: ',r_squaredgKurz)
resfLang = PLang - f(wLang, *paramfLang)
ss_resfLang = np.sum(resfLang**2)
ss_totLang = np.sum((PLang-np.mean(PLang))**2)
r_squaredfLang = 1 - (ss_resfLang / ss_totLang)
print('Gute fLang: ',r_squaredfLang)
resgLang = PLang - g(wLang, *paramgLang)
ss_resgLang = np.sum(resgLang**2)
r_squaredgLang = 1 - (ss_resgLang / ss_totLang)
print('Gute gLang: ',r_squaredgLang)

# Der Fit mit der e-Funktion ist schlechter.


### Plot
w = np.linspace(0.1,26,1000)
plt.plot(wLang, PLang, 'mx', label ='Lang Messwerte')
plt.plot(w,g(w,*paramgLang), 'r', label = 'Lang Fit')
plt.plot(wKurz, PKurz, 'cx', label ='Kurz Messwerte')
plt.plot(w,g(w,*paramgKurz), 'b', label = 'Kurz Fit')
plt.plot(w, 0*w, 'k')
plt.plot(wKurz, alpha, 'k.', label = 'Alpha')
plt.xlim(0.1,26)

plt.xlabel(r'$\omega \ \mathrm{in} \ \mathrm{MHz}$')
plt.ylabel(r'')

plt.legend(loc='best')
#plt.savefig('RLC_DirekteMessung/build/PlotR.pdf')
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
write('RLC_DirekteMessung/build/LTheorie.tex', make_SI(Lconst*10**9, r'\nano\farad\per\meter', figures = 1))
write('RLC_DirekteMessung/build/GTheorie.tex', make_SI(Gconst*10**9, r'\nano\siemens\per\meter', figures = 1))

