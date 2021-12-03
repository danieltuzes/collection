import math
from scipy.special import gamma, gammainc
import numpy as np
import matplotlib.pyplot as plt


def lorenz(x, y, z, a=10, b=8/3, c=28):
    x_dot = a*(y - x)
    y_dot = - y + c*x - x*z
    z_dot = -b*z + x*y
    return x_dot, y_dot, z_dot


dt = 0.01
num_steps = 10000
# Need one more for the initial values
xs = np.empty(num_steps + 1)
ys = np.empty(num_steps + 1)
zs = np.empty(num_steps + 1)

# Set initial values
xs[0], ys[0], zs[0] = (1, 1, 1)
# Step through "time", calculating the partial derivatives at the current point
# and using them to estimate the next point
for i in range(num_steps):
    x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + (x_dot * dt)
    ys[i + 1] = ys[i] + (y_dot * dt)
    zs[i + 1] = zs[i] + (z_dot * dt)


def count_ones_zeroes(bits):
    ones = 0
    zeroes = 0
    for bit in bits:
        if (bit == 1):
            ones += 1
        else:
            zeroes += 1
    return (zeroes, ones)


def runs_test(bits):
    n = len(bits)
    zeroes, ones = count_ones_zeroes(bits)

    prop = float(ones)/float(n)
    print("  prop ", prop)

    tau = 2.0/math.sqrt(n)
    print("  tau ", tau)

    if abs(prop-0.5) > tau:
        return (False, 0.0, None)

    vobs = 1.0
    for i in range(n-1):
        if bits[i] != bits[i+1]:
            vobs += 1.0

    print("  vobs ", vobs)

    p = math.erfc(abs(vobs - (2.0*n*prop*(1.0-prop))) /
                  (2.0*math.sqrt(2.0*n)*prop*(1-prop)))
    success = (p >= 0.01)
    return (success, p, None)


print(runs_test(xs))


def monobit_test(bits):
    n = len(bits)

    zeroes, ones = count_ones_zeroes(bits)
    s = abs(ones-zeroes)
    print("  Ones count   = %d" % ones)
    print("  Zeroes count = %d" % zeroes)

    p = math.erfc(float(s)/(math.sqrt(float(n)) * math.sqrt(2.0)))

    success = (p >= 0.01)
    return (success, p, None)


print(runs_test(xs))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(xs, ys, zs)
