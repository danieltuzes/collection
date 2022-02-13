"""Search for prime numbers. Can be inefficient."""


def isprime(check, primes) -> bool:
    """docs"""
    for prime in primes:
        if (check % prime) == 0:
            return False
    return True


def main():
    primes = []
    i = 2
    while True:
        if isprime(i, primes):
            primes.append(i)
            print(i)

        i += 1


if __name__ == "__main__":
    main()
