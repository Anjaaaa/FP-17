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


### Umrechnung 10MHz
# mA pro cm
Messung10 = [(233-29)/4.9,(446-23)/5.1,(664-446)/5.3,(900-664)/5.7]
scale10 = ufloat(np.mean(Messung10), np.sqrt(np.std(Messung10)))
print(scale10)
#a10 = ufloat()
