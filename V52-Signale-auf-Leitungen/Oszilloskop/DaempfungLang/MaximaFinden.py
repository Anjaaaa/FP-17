import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

x, y = np.genfromtxt('F0042MTH.txt', unpack = True)
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
# Zwei Punkte sind irgendwie nocht falsch. Sie werden jetzt entfernt.
xNew = np.delete(xNew, 1)
xNew = np.delete(xNew, 1)
yNew = np.delete(yNew, 1)
yNew = np.delete(yNew, 1)
# Manche Maxima wurden doppelt gezählt, daher müssen sie entfernt werden.

for i in range(0,len(yNew)):
    print('i',i)
    if len(yNew)<i:
        print('Break i')
        break
    else:
        for j in range(i+1,len(yNew)-1):
            print('j',j)
            print('len(yNew)',len(yNew))
            if len(yNew)<j:
                print('Break j')
                break
            elif yNew[i] == yNew[j]:
                print('Delete ',i,j)
                yNew = np.delete(yNew,j)
                xNew = np.delete(xNew,j)
                j -= 1

plt.plot(xNew, yNew, 'bo', ms = 1)
plt.savefig('Bereinigt.pdf')
plt.show()

f = open("DatenLang.txt", "w")
f.write( "# omega P" + "\n"  )
f.write( "# Hz dB" + "\n"  )
for i in range(0,len(xNew)):
    f.write( str(xNew[i]) + " " + str(yNew[i]) + "\n")
f.close()
