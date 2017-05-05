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
        
x_00, I_00 = np.genfromtxt('Daten/Daten_TEM_00.txt', unpack = True)
x_01, I_01 = np.genfromtxt('Daten/Daten_TEM_01.txt', unpack = True)


#Funktion für die Intensität der TEM_00 (a = I_0, b = strahbreite):
def funktion_00(x, a, b, c):
	return a * np.exp(-2 * (x+c)**2 / b**2)
	
params, cov = curve_fit(funktion_00, x_00, I_00)
print(params)
print(cov)

ort_00 = np.linspace(-15, 15, 200)
plt.plot(ort_00, funktion_00(ort_00, params[0], params[1], params[2]), 'g-', label='Fit')
plt.plot(x_00, I_00, 'rx', label = 'Messdaten')
plt.ylabel('Intensität in nA')
plt.xlabel('Position in mm')
plt.xlim(-15 , 15)

plt.legend(loc = 'best')

plt.savefig('build/TEM_00.png')
plt.close()


#daten für latex auslesen:
a = ufloat(params[0], np.sqrt(cov[0,0]))
b = ufloat(params[1], np.sqrt(cov[1,1]))
c = ufloat(params[2], np.sqrt(cov[2,2]))
write('build/TEM_00_a.tex', make_SI(a, r'\nano\ampere'))
write('build/TEM_00_b.tex', make_SI(b, r'\milli\meter'))
write('build/TEM_00_c.tex', make_SI(c, r'\milli\meter'))

write('build/tab_TEM_00.tex', make_table([x_00, I_00], [1,2]))
write('build/tab_TEM_00_gesamt.tex', make_full_table(
r'Intensität der TEM$_{00}$-Mode entlang der x-Achse',
'tab:TEM_00',
'build/tab_TEM_00.tex',
[],
[ r'x in \si{\milli\meter}', r'I in \si{\nano\ampere}']))









#Funktion für die Intensität der TEM_01:
def funktion_01(x, a, b, c, d, e):
	return a * np.exp(-2 * (x+c)**2 / b**2) + d * np.exp(-2 * (x+e)**2 /b**2)
	
params, cov = curve_fit(funktion_01, x_01, I_01, (50, 1.5, 1, 50, 3))
#schätzwerte sind an dieser stelle sehr wichtig!!
print(params)
print(cov)


ort_01 = np.linspace(-22,16, 200)

plt.plot(ort_01, funktion_01(ort_01, params[0], params[1], params[2], params[3], params[4]), 'g-', label='Fit')
plt.plot(x_01, I_01, 'rx', label='Messdaten')
plt.xlim(-22,16)
plt.ylabel('Intensität in nA')
plt.xlabel('Position in mm')
plt.legend(loc = 'best')
plt.savefig('build/TEM_01.png')
plt.close()

#daten für latex auslesen:
a01 = ufloat(params[0], np.sqrt(cov[0,0]))
b01 = ufloat(params[1], np.sqrt(cov[1,1]))
c01 = ufloat(params[2], np.sqrt(cov[2,2]))
d01 = ufloat(params[3], np.sqrt(cov[3,3]))
e01 = ufloat(params[4], np.sqrt(cov[4,4]))
write('build/TEM_01_a.tex', make_SI(a01, r'\nano\ampere'))
write('build/TEM_01_b.tex', make_SI(b01, r'\milli\meter'))
write('build/TEM_01_c.tex', make_SI(c01, r'\milli\meter'))
write('build/TEM_01_d.tex', make_SI(d01, r'\nano\ampere'))
write('build/TEM_01_e.tex', make_SI(e01, r'\milli\meter'))

write('build/tab_TEM_01.tex', make_table([x_01, I_01], [1,2]))
write('build/tab_TEM_01_gesamt.tex', make_full_table(
r'Intensität der TEM$_{01}$-Mode entlang der x-Achse',
'tab:TEM_01',
'build/tab_TEM_01.tex',
[],
[r'I in \si{\nano\ampere}', r'x in \si{\milli\meter}']))


