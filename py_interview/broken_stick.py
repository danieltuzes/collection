"""Eltörünk egy botot n részre, a töréspontokat
a teljes hosszon egyeneltes eloszlás szerint megválasztva,
és nézzük meg, hogy az n-edik legrövidebbnek mi a várható
értéke."""
import random
import sys


def main() -> None:
    """docs"""

    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = int(input("Number of breakpoints: "))

    random.seed(0)

    nth_lengths_sum = [0 for _ in range(n+1)]  # the nth smallest piece
    iterations = 100
    total = 0
    while True:
        total += iterations
        for _ in range(iterations):
            x = [0, 1]  # break points
            for _ in range(n):
                x.append(random.random())
            x.sort()
            lengths = [x[i+1]-x[i] for i in range(n+1)]
            lengths.sort()
            for i, length in enumerate(lengths):
                nth_lengths_sum[i] += length

        for nth_length_sum in nth_lengths_sum:
            print(nth_length_sum/total, end="\t")
        print()

        iterations *= 2


if __name__ == "__main__":
    sys.exit(main())
