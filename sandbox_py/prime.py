"""
    Print out prime numbers up to a desired value.
    
    It also serves as an example how to compile code with nuitka
    To compile this code, run `python -m nuitka --mingw64 prime.py`
    Read more: https://github.com/Nuitka/Nuitka
"""

import math # for sqrt
import time # to measure time

def get_primes(num: int, last_only: bool) -> None:
    """Prints out prime numbers up to num. Algorithm is naiive.

        Parameters
        -------------
        num : int
            Prime numbers will be printed out until this number

        last_only : bool
            Tells whether only the last prime number should be printed out.
            Useful to make speed tests because many times printing into the terminal
            takes the vast majority of the time.

        Return
        -------------
        void
            No return value is provided
            but primes number will be printed onto the standard output"""
    largest_prime = 2   # will be overwritten

    for nominee in range(2, num):
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


def get_primes_fast(num: int, last_only: bool) -> None:
    """Prints out prime numbers up to num in a faster way.

        This version uses more memory but faster than the other method get_primes,
        because it only tries to divide the pivot number (called nominee)
        by the prime numbers stored in in the array primes.

        Parameters
        -------------
        num : int
            Prime numbers will be printed out until this number

        last_only : bool
            Tells whether only the last prime number should be printed out.
            Useful to make speed tests because many times printing into the terminal
            takes the vast majority of the time.

        Return
        -------------
        void
            No return value is provided
            but primes number will be printed onto the standard output"""
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
    for i in range(5):
        start_time = time.time()
        get_primes_fast(1000000, True)
        print("Runtime: %s s" % (time.time() - start_time))