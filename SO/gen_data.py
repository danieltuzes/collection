"""Reply to a question on SO.

https://stackoverflow.com/questions/69530586/fitting-exponential-function-in-gnuplot/69542855
"""

import math
import numpy as np

A = 30
b = 1/1000
T = 500
phi = 0.3
S = 140


def f(x):
    """f(x)=A*exp(-b*x)*sin(2*pi*x/T+phi)+S"""

    return A*math.exp(-b*x)*math.sin(2*math.pi*x/T+phi)+S


np.random.seed(0)
with open("data.txt", mode="w", encoding="utf-8") as ofile:
    for i in range(0, 1600, 50):
        print(i, f(i+np.random.random(1)[0]/10) +
              np.random.random(1)[0], 0, file=ofile)
