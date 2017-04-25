import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat
import matplotlib.pyplot as plt
from scipy.stats import sem #fehler des mittelwertes
from table import (
        make_table,
        make_full_table,
        make_SI,
        write)


ordnung, a_rechts, a_links = np.genfromtxt("Daten/Daten_Interferenz.txt", unpack = True)


#Mittelwert Abstand ausrechnen:
a = (a_rechts + a_links)/2

#Winkel der Maxima ausrechnen:
# Der Abstand zum Schirm beträgt 104cm

phi = np.arctan(a / 104)

#gitterkonstante 100/mm umrechnen in nm
g = 10**(-5)

#wellenlänge lambda ausrechnen:
l = np.zeros(np.size(a))

for i in range (1, np.size(a)+1):
	l[i-1] = g * np.sin(phi[i-1]) / ordnung[i-1]
	

print (np.mean(l), '+-', sem(l))

l_gesamt = ufloat(np.mean(l), sem(l))

#Daten für Latex exportieren

write('build/wellenlaenge.tex', make_SI(l_gesamt*10**9, r'\nano\meter', figures=2))

write('build/tab_wellenlaenge.tex', make_table([ordnung, a_rechts, a_links, l*10**9],[0,2,2,2]))

write('build/tab_wellenlaenge_gesamt.tex', make_full_table(
r'Berechnung der Wellenlänge $\lambda$ durch die Abstände der Interferenzmaxima',
'tab:Wellenlaenge',
'build/tab_wellenlaenge.tex',
[],
[r'Ordnung Maximum ', r'Abstand $a$ rechts in \si{\centi\meter}', r'Abstand $a$ links in \si{\centi\meter}', r'$\lambda$ in $\si{\nano\meter}$']))




