import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

x, y = np.genfromtxt('F0041MTH.txt', unpack = True)
ymax = argrelextrema(y,np.greater_equal)

a = 0
for i in range(0,len(y)):
    if y[i]<=-38:
        y[i] = 0
    for j in range(0,len(ymax[0])):
        if i==ymax[0][j]:
            a = 1
    if a == 0:
        y[i] = 0
    a = 0

xNew = []
yNew = []
for i in range(0,len(y)):
    if y[i]!=0:
        xNew.append(x[i])
        yNew.append(y[i])
plt.plot(xNew, yNew, 'bo', ms = 1)
plt.savefig('Bereinigt.pdf')
plt.show()
