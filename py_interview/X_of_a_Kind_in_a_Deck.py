"""In a deck of cards, each card has an integer written on it.

Return true if and only if you can choose X >= 2 such that it is possible to split the entire deck into 1 or more groups of cards, where:

Each group has exactly X cards. All the cards in each group have the same integer."""


import math
USE_MATH = False


def get_prime_factors(target: int) -> dict[int, int]:
    i = 2
    divisors = dict()
    while target > 1:
        while target % i == 0:
            if i in divisors:
                divisors[i] += 1
            else:
                divisors[i] = 1
            target //= i
        i += 1
    return divisors


def intersect(a: dict, b: dict) -> dict:
    inters = dict()
    for key in a:
        if key in b:
            inters[key] = min(a[key], b[key])

    return inters


def mygcd(values: list[int]):
    divisors_list = []
    for value in values:
        divisors_list.append(get_prime_factors(value))

    common_divisors = divisors_list[0]
    for divisors in divisors_list:
        common_divisors = intersect(common_divisors, divisors)

    gcd = 1
    for val in common_divisors:
        gcd *= val

    return gcd


def main():
    while True:
        inputtext = input("Give the list of vals separated with ,: ")
        val_strs = inputtext.split(",")
        val_counter = dict()
        for val_s in val_strs:
            val = int(val_s)
            if val in val_counter:
                val_counter[val] += 1
            else:
                val_counter[val] = 1

        if USE_MATH:
            if math.gcd(*val_counter.values()) > 1:
                print(True)
            else:
                print(False)
        else:
            if mygcd(val_counter.values()) > 1:
                print(True)
            else:
                print(False)


if __name__ == "__main__":
    main()
