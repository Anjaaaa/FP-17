import numpy as np
import matplotlib.pyplot as plt

x, y = np.genfromtxt('F0041MTH.txt', unpack = True)

plt.plot(x, y, 'bo', ms = 1)
plt.savefig('F0054CH1.pdf')
plt.show()
