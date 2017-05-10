import numpy as np
from uncertainties import ufloat



### Umrechnung 10MHz
# Abstand in mA geteilt durch den Abstand in cm
Messung10 = [(233-29)/4.9,(446-233)/5.1,(664-446)/5.3,(900-664)/5.7]
# Mittelwert
scale10 = ufloat(np.mean(Messung10), np.sqrt(np.std(Messung10)))
# Abstand der Maxima vom ersten Punkt (hier 29)
a10 = ufloat(4.9,0.1)
b10 = ufloat(6.7,0.1)
# Wert in mA = Abstand zu 29 in mA umrechnen + 29
a10 = a10*scale10 + 29
b10 = b10*scale10 + 29


### Umrechnung 15MHz
# Abstand in mA geteilt durch den Abstand in cm
Messung15 = [(293-208)/5.1,(371-293)/4.7,(467-371)/5.7,(568-467)/6.0]
# Mittelwert
scale15 = ufloat(np.mean(Messung15), np.sqrt(np.std(Messung15)))
# Abstand der Maxima vom ersten Punkt (hier 208)
a15 = ufloat(8.9,0.4)
b15 = ufloat(11.9,0.2)
# Wert in mA = Abstand zu 208 in mA umrechnen + 208
a15 = a15*scale15 + 208
b15 = b15*scale15 + 208


### Umrechnung 20MHz
# Abstand in mA geteilt durch den Abstand in cm
Messung20 = [(473-341)/7.3,(518-473)/2.5,(619-518)/5.6,(705-619)/4.7]
# Mittelwert
scale20 = ufloat(np.mean(Messung20), np.sqrt(np.std(Messung20)))
# Abstand der Maxima vom ersten Punkt (hier 341)
a20 = ufloat(6.2,0.4)
b20 = ufloat(11.3,0.1)
# Wert in mA = Abstand zu 341 in mA umrechnen + 341
a20 = a20*scale20 + 341
b20 = b20*scale20 + 341


### Umrechnung 25MHz
# Abstand in mA geteilt durch den Abstand in cm
Messung25 = [(585-516)/4.5,(668-585)/5.3,(751-668)/5.7,(849-751)/6.5]
# Mittelwert
scale25 = ufloat(np.mean(Messung25), np.sqrt(np.std(Messung25)))
# Abstand der Maxima vom ersten Punkt (hier 516)
a25 = ufloat(4.7,0.5)
b25 = ufloat(7.7,0.5)
# Wert in mA = Abstand zu 516 in mA umrechnen + 516
a25 = a25*scale25 + 516
b25 = b25*scale25 + 516


### Umrechnung 30MHz
# Abstand in mA geteilt durch den Abstand in cm
Messung30 = [(639-576)/4.1,(718-639)/5.2,(814-718)/6.2,(908-814)/6.2]
# Mittelwert
scale30 = ufloat(np.mean(Messung30), np.sqrt(np.std(Messung30)))
# Abstand der Maxima vom ersten Punkt (hier 576)
a30 = ufloat(9.2,0.6)
b30 = ufloat(13.8,0.4)
# Wert in mA = Abstand zu 576 in mA umrechnen + 576
a30 = a30*scale30 + 576
b30 = b30*scale30 + 576



f = open("Daten.txt", "w")
f.write( "# nu_osc nu_e erstes_max Fehler zweites_max Fehler" + "\n"  )
f.write( "# MHz MHz mA mA mA mA" + "\n"  )
f.write( "10    " + "10.588 " + str(a10.nominal_value) + " " + str(a10.std_dev) + " " +  str(b10.nominal_value) + " " + str(b10.std_dev) + " " +  "\n"  )
f.write( "15.35 " + "15.970 " + str(a15.nominal_value) + " " + str(a15.std_dev) + " " + str(b15.nominal_value) + " " + str(b15.std_dev) + " " +   "\n"  )
f.write( "20    " + "20.56  " + str(a20.nominal_value) + " " + str(a20.std_dev) + " " + str(b20.nominal_value) + " " + str(b20.std_dev) + " " +   "\n"  )
f.write( "24.44 " + "23.87  " + str(a25.nominal_value) + " " + str(a25.std_dev) + " " + str(b25.nominal_value) + " " + str(b25.std_dev) + " " +   "\n"  )
f.write( "30    " + "29.42  " + str(a30.nominal_value) + " " + str(a30.std_dev) + " " + str(b30.nominal_value) + " " + str(b30.std_dev) + " " +   "\n"  )
f.close()
