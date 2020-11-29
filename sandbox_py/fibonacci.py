"""
    Write a simple module that prints out the Fibonacci numbers up to a desired value.
"""


def fibonacci(num):
    """Prints out Fibonacci numbers till n"""
    generator_1 = 0
    generator_2 = 1
    while generator_1 < num:
        print(generator_1, end=" ")
        generator_1, generator_2 = generator_2, generator_1+generator_2
    print()


if __name__ == "__main__":
    fibonacci(300)
