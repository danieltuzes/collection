# illusion

[question](https://stackoverflow.com/questions/69507141/how-to-generate-non-overlapping-random-points-uniformly-and-evenly-within-n-dime)

## answer

To better understand the question and give some hints on possible causes of your problem, I post this answer which cannot fit into a comment.

## Description

Let me use my own words to explain your problem and please correct me or your answer to make your case more clear.

You are given *N_1* and *N_2* number of points in an *M* dimensional space. Maybe your points in each set are normally distributed in the *M* dimensional space, e.g. if you create it with [make_blobs](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_blobs.html). Then you identify the minimum values *x_{i,min,1}* and maximum values *x_{i,max,1}* for each dimension *x_i* for each point in the set *N_1*. Then you generate random points in the *M* dimensional space within the *M*-dimensional rectangle restricted in the range [x_{1,min,1},x_{1,max,1}] x [x_{2,min,1},x_{2,max,1}] x ... x [x_{M,min,1},x_{M,max,1}]. Then you apply PCA and plot the 2 principal components. Your observation is your random points are not uniformly distributed within the range where your data lies.

## Explanation and example in 2D

If your data follows an *M*-dimensional normal distribution (in this example, *M*=2), the minimum and maximum values can lie couple of times further than the standard deviation. When you generate random points within the minimum and maximum values, your random points will evenly represent the ranges where you barely have data points. Take the following as an example. It generates 10'000 data points with a normal distribution in 2D, and then generates 5 further points with uniform distribution in the rectangle drawn around the data points.

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(3)
x_data = np.random.normal(size=10000)
x_min = x_data.min()
x_max = x_data.max()

y_data = np.random.normal(size=10000)
y_min = y_data.min()
y_max = y_data.max()

random_x = np.random.uniform(x_min, x_max, size=5)
random_y = np.random.uniform(y_min, y_max, size=5)

fig, ax = plt.subplots()
ax.plot(x_data[:10000], y_data[:10000], "o",
        label="data points with normal distribution")
ax.plot(random_x, random_y, "o", label="random points with uniform distribution")
ax.legend()
plt.show()
```

Although the random points are uniformly distributed, one may think they are only at the edges of the distribution.

## Suggestion

If I understood your problem correctly and the problem is just an illusion, please rephrase your question accordingly so that others can address your specific request.

If you want your random points to better reflect the distribution properties of your data, you need to set up a model on your data, e.g. it is a normally distributed data points. Identify the mean and std, and generate random points using a distribution with that properties.

## Further questions

- Could you please show more data points?
- Is it relevant that you have 2 datasets?
- I didn't understand the figure here:
  > the red one is the position required for the black points which are crossed"
  Could you please replot your figure, provide more example and rephrase the legend?
