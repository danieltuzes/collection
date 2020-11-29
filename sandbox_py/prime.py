"""
    Print out prime numbers up to a desired value.
"""

import math


def get_primes(num, last_only):
    """Prints out prime numbers up to n"""

    for nominee in range(2, num):
        divisor = 2
        for divisor in range(2, int(math.sqrt(nominee))):
            if nominee % divisor == 0:
                break
        else:
            if not last_only:
                print(nominee, sep=" ")
            else:
                largest_prime = nominee

    if last_only:
        print(largest_prime)


def get_primes_fast(num, last_only):
    """Prints out prime numbers up to n, trying to divide with primes only."""
    primes = [2]

    for nominee in range(3, num):
        for prime in primes:
            if prime > math.sqrt(nominee):
                primes.append(nominee)
                if not last_only:
                    print(nominee, sep=" ")
                break
            if nominee % prime == 0:
                break

    if last_only:
        print(primes[-1])


if __name__ == "__main__":
    get_primes(1000000, True)
