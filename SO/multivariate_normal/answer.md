# answer

question:
https://stackoverflow.com/questions/69902269/how-to-generate-multivariate-normal-distribution-from-a-standard-normal-value

Your code is almost correct, but you can check that your numbers don't have the desired covariance property, if you apply [numpy's `cov`](https://numpy.org/doc/stable/reference/generated/numpy.cov.html) function:

```python
res = np.array([n1,n2]).T.dot(B) + A
np.cov(res.T).round()
# returns ~ 
# array([[5., 2.],
#        [2., 1.]])
```

Note that the elements 1,1 and 2,2 are exchanged compared to the desired value.

To leverage numpy's CPU-vectorized matrix multiplication, you use [numpy's `dot`](https://numpy.org/doc/stable/reference/generated/numpy.dot.html?highlight=dot#numpy.dot) function. You properly arranged the N pieces of 2D input vectors Z into a Nx2 dimensional vector `np.array([n1,n2]).T`. But as you pointed out in the [Cholesky decomposition and variance](https://math.stackexchange.com/questions/1344788/cholesky-decomposition-and-variance) question, the Z values have to be multiplied by B from the left, and you also would like to incorporate it into the `dot` function's broadcasting rule, and the problem lies here. The code `np.array([n1,n2]).T.dot(B)` multiplies the (array of) Z from the right, not from the left. To compute the left-product by B, you need to use `dot(B.T)`

This example also shows that the covariance matrix has the right form. I also fixed the seed to make the results reproducible.

```python
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
```

In the fig. below the random points are plotted, together with the eigenvectors of the covariance matrix with a length of the square root of their eigenvalues, like on [Wikipedia](https://en.wikipedia.org/wiki/File:GaussianScatterPCA.svg).
