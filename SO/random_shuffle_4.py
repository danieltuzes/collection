import random
random.seed(1)

groups = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0,
    'E': 0
}

str_options = [*groups]*4
random.shuffle(str_options)
print(str_options)
