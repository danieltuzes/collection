import random
import numpy as np

random.seed(0)
N=10000

V = np.array([
    [1, 2],
    [2, 5]])
B = np.linalg.cholesky(V)
A = np.array([1, 2])

# norm() return one number from standard normal distribution
n1 = np.array([random.gauss(0, 1) for _ in range(10000)])
n2 = np.array([random.gauss(0, 1) for _ in range(10000)])
res = np.array([n1, n2]).T.dot(B.T) + A

np.cov(res.T).round()
# returns ~  array([[1., 2.],
#                   [2., 5.]])