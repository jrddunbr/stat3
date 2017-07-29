import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from time import sleep, clock
import threading
import datetime
import os

from os import listdir
from os.path import isfile, join

from multiprocessing import Process

def graph(datapath, imagepath, title):

    x = []
    y1 = []
    y2 = []

    data = open(datapath)

    biggest = 0

    for line in data:
        try:
            field = line.split("-")

            time = field[0].split(":")
            timef = int(time[0]) + int(time[1])/60.0 + int(time[2])/60.0/60.0
            x.append(timef)

            upload = float(field[1])
            y2.append(0 - upload)

            download = float(field[2])
            y1.append(download)

            speed = float(field[3].strip())
            if speed > biggest:
                biggest = speed

        except Exception as e:
            print("data processing\n{}".format(e))

    if biggest > 0:
        plt.plot(x, y1, "black", x, y2, "black")
        fig, ax = plt.subplots()
        ax.fill_between(x,y1, color='#aaaaff')
        ax.fill_between(x,y2, color='#ffaaaa')
        ax.axis([0,24, 0 - biggest, biggest])
        ax.set_xlabel('Time (GMT)')
        ax.set_ylabel('<- Upload  Speed (Mbit/s)  Download ->')
        ax.set_title(title)
        plt.xticks(range(0,24))
        ax.grid(color='#666666', linestyle='dotted', linewidth=1)
        fig.tight_layout()
        fig.set_size_inches(22, 17)

        plt.savefig(imagepath, dpi=300)

if __name__ == '__main__':

    path = "/opt/stat/data/high/"

    image = "/opt/stat/data/image/high"

    proc = []

    directory = [f for f in listdir(path) if isfile(join(path, f))]
    for datafile in directory:
        datapath = path + datafile
        imagepath = image + "/" + datafile + ".png"
        p = Process(target=graph, args=(datapath,imagepath, "",))
        p.start()
        proc.append(p)
        sleep(1)

    while 1:
        allclosed = True
        for process in proc:
            if process.is_alive():
                allclosed = False
        if allclosed:
            print("All processes closed successfully")
            exit(0)
