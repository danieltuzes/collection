"""Írj egy numerikus szimulációt, ami a következő játékot játsza.

A 0-s mezőből indulsz és annyit lépsz előre, ahanyast dobsz egy dobókockával.
A kérdés, hogy az összes játékhoz képest a játékok mekkora részében lépsz
egy előre megadott mezőbe? Legyen ennek az értéke N!
Ennek segítségével megadható, hogy empirikusan mekkora a valószínűsége,
hogy egy adott mezőbe lépsz.

A program vegye az első hívási argumentumot az N értékének,
vagy ha nincs megadva hívási paraméterként, akkor kérje be a standard inputról.
Majd írja ki, hogy 10, 100, ... stb játékra vetítve, hogy
az esetek hanyad részében lép a program N-be!

Lehet megadni második paramétert is, amely megadja, hogy teljes
eloszlást számoljon-e és ábrázoljon a program N-ig.
Az 1, y és i értékek igazat jelentenek, minden más hamisat."""

import random
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
random.seed(0)


def hit(target: int) -> int:
    """If dice hits, return 1, 0 otherwise."""
    dice_sum = 0
    while dice_sum < target:
        dice_sum += random.randint(1, 6)
        if dice_sum == target:
            return 1
    return 0


def single_hit(target: int) -> None:
    total_hit = 0

    iterations = 0
    itermax = 10
    while True:
        for _ in range(itermax):
            total_hit += hit(target)
            iterations += 1
        itermax *= 2
        print(total_hit/iterations)


def distr(target: int) -> None:
    hits = defaultdict(lambda: 0)
    itermax = 10
    while True:
        for _ in range(itermax):
            total = 0
            while total <= target:
                hits[total] += 1
                total += random.randint(1, 6)
        itermax *= 2
        fig, ax = plt.subplots()
        ax.bar(list(hits.keys())[1:], [val/hits[0]
               for val in hits.values()][1:], width=1.)
        ax.axhline(2/7, linestyle='-', color='k')
        ax.set_xticks(range(1, target, target//6))
        plt.savefig("plt.png")
        input("press any key")


def main() -> None:
    if len(sys.argv) > 1:
        target = int(sys.argv[1])
    else:
        target = int(input("Target value: "))
    if len(sys.argv) > 2:
        distr_str = sys.argv[2]
    else:
        distr_str = input("Do you want distribution plot (y/n)? ")

    if distr_str in ["y", "1", "i"]:
        distr(target)

    single_hit(target)


if __name__ == "__main__":
    sys.exit(main())
