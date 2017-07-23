import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from time import sleep, clock
import threading
import datetime
import os



x = []
y1 = []
y2 = []


# import random
# for i in range(0,20):
#     x.append(i)
#     y1.append(random.randint(0,100))
#     y2.append(random.randint(-100,0))


data = open("/home/jared/7-23-2017:128.153.145.251-1")

biggest = 0

for line in data:
    try:
        field = line.split("-")

        time = field[0].split(":")
        timef = int(time[0]) + int(time[1])/60 + int(time[2])/360
        #timef = datetime.datetime(year=2017,month=7,day=23,hour=int(time[0]),minute=int(time[1]))
        x.append(timef)

        upload = float(field[1])
        y2.append(0 - upload)

        download = float(field[2])
        y1.append(download)

        speed = int(field[3])
        if speed > biggest:
            biggest = speed

    except Exception as e:
        print(e)


plt.plot(x, y1, x, y2)
fig, ax = plt.subplots()
ax.fill_between(x,y1, color='#aaaaff')
ax.fill_between(x,y2, color='#ffaaaa')

ax.axis([0,24, 0 - biggest, biggest])
ax.set_xlabel('Time')
ax.set_ylabel('Speed (Mbit/s)')
ax.set_title(r'SWM1 to sc334-a')
plt.xticks(range(0,24))
ax.grid(color='#666666', linestyle='dotted', linewidth=1)

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
fig.set_size_inches(20, 20)
plt.savefig('foo.png', dpi=300)
