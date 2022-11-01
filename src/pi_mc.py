import random
import numpy as np
import matplotlib.pyplot as plt
import math

pi_mean = []
pi_std = []

for n in range(1000,1001000,10000):
    print(n)
    experimentos = []
    for _ in range(30):
        parejas = [(random.random(),random.random()) for i in range(n)]

        count = 0

        for x, y in parejas:
          if x * x + y * y < 1:
            count += 1

        pi = (count/n) * 4
        experimentos.append(pi)

    pi_mean.append(np.mean(experimentos))
    pi_std.append(np.std(experimentos))
    print("Pi mean {}".format(np.mean(experimentos)))
    print("Pi std {}".format(np.std(experimentos)))

fig, ax = plt.subplots(1)
t = range(1000,1001000,10000)
pi_mean = np.array(pi_mean)
pi_std  = np.array(pi_std)

ax.plot(t, pi_mean, lw=2, label='Valor medio de Pi', color='blue')
ax.fill_between(t, pi_mean+pi_std, pi_mean-pi_std, facecolor='blue', alpha=0.5)
plt.axhline(y=math.pi, color='r', linestyle='--', alpha = 0.7)
ax.set_title(r'Pi estimado mediante método de Monte Carlo')
ax.legend(loc='upper right')
ax.set_xlabel('N')
ax.set_ylabel('Valor estimado de Pi')
plt.show()
