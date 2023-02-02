"""Klenke Exercise 8.1.2

Teltházas, n férőhelyes színházba egyesével érkeznek a vendégek.
Az első vendég random választ helyet, minden következő pedig
a jegyének megfelelő helyet, ha szabad, vagy random másikat.

- Mekkora az esélye, hogy az utolsó vendég a saját helyére ülhet?
- Mekkora az esélye, hogy az m. vendég a saját helyére ülhet?
"""
import random
import math

n = int(input("Férhőhelyek száma (n): "))
seed = input("seed: ")
random.seed(seed)

was_free = 0
digits = 1
for j in range(10**10):
    seats = [False for _ in range(n)]
    seats[int(random.randrange(0,n))] = True
    for i in range(1,n-1):
        if seats[i]:
            nominee = random.randrange(0,n)
            while seats[nominee]:
                nominee = random.randrange(0,n)
            seats[nominee] = True
        else:
            seats[i] = True

    if seats[n-1]:
        was_free += 1
    
    if math.log(j+1) > digits:
        print(was_free/j)
        digits +=1
