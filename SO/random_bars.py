import random
import matplotlib.pyplot as plt

random.seed(0)

ITER = 20
LOW = 0
HIGH = 10

RND_NUMS = []
for _ in range(ITER):
    RND_NUMS.append(random.randint(LOW, HIGH))

ax = plt.axes()
ax.set_facecolor('white')
plt.hist(RND_NUMS, bins=range(0, 10))
