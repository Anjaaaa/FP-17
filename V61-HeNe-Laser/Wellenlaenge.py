import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.stats import sem #fehler des mittelwertes
from table import (
        make_table,
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

write('build/wellenlaenge.tex', make_SI(np.mean(l), r'\nano\meter', figures=2))




