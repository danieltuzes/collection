"""https://stackoverflow.com/questions/70915526/python-async-random-broken/70918654#70918654"""

import random
import matplotlib.pyplot as plt

length_of_longest = []

for j in range(1000):
    random.seed(j)
    rndstr = "".join([str(random.randint(0, 4)) for _ in range(42)])
    for i in range(1, 42):
        total = 0
        for my_str in "1234":
            for_my_str = rndstr.count(my_str*i)
            total += for_my_str
        if total == 0:
            length_of_longest.append(i-1)
            break

plt.hist(length_of_longest, bins=range(0, max(length_of_longest)))
