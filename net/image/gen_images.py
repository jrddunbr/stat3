import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from time import sleep, clock
import threading
import datetime
import os

import random



np.random.seed(0)

x = []
y1 = []
y2 = []

for i in range(0,20):
    x.append(i)
    y1.append(random.randint(0,100))
    y2.append(random.randint(-100,0))

fig, ax = plt.subplots()

plt.plot(x, y1, x, y2)
d = 0
ax.fill_between(x,y1, color='#aaaaff')
ax.fill_between(x,y2, color='#ffaaaa')

ax.axis([0,20,-1000,1000])
ax.set_xlabel('Time')
ax.set_ylabel('Speed (Mbit/s)')
ax.set_title(r'SWM1 to sc334-a')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.savefig('foo.png')
