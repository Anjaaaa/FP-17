import numpy as np
import matplotlib.pyplot as plt

x, y = np.genfromtxt('F0054CH1.txt', unpack = True)

plt.plot(x, y, 'b.')
plt.savefig('F0054CH1.pdf')
plt.show()
