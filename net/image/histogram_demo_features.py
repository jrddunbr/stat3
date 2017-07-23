import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

np.random.seed(0)

# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
x = mu + sigma * np.random.randn(5000)

num_bins = 500

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, normed=1)

ax.set_xlabel('Time')
ax.set_ylabel('Speed (Mbit/s)')
ax.set_title(r'SWM1 to sc334-a')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.savefig('foo.png')
