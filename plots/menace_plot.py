#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('reinforcements_new.csv', sep=',', header=None)
data = pd.DataFrame(data)

x = data[0]
y = data[1]

#n = 10000
#n = 1000
#n = 240
n = 100

x = x[:n]
y = y[:n]

plt.scatter(x, y, c='black', marker='.')
plt.xlabel('number of games')
plt.ylabel('cumulative reinforcements')
#plt.show()
plt.savefig("reinforcements_new_100.svg")
