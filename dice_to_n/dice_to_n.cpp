// dice_to_n.cpp : This file contains the 'main' function. Program execution begins and ends there.
// Írj egy numerikus szimulációt, ami a következő játékot játsza. Az 0-s mezőből indulsz és annyit lépsz előre, ahanyast dobsz egy dobókockával. A kérdés, hogy az összes játékhoz képest a játékok mekkora részében lépsz egy előre megadott mezőbe? Legyen ennek az értéke N! Ennek segítségével megadható, hogy empirikusan mekkora a valószínűsége, hogy egy adott mezőbe lépsz. A program vegye az első és egyetlen hívási argumentumot az N értékének, vagy ha nincs megadva hívási paraméterként, akkor kérje be a standard inputról. Majd írja ki, hogy 10, 100, ... stb játékra vetítve az esetek hanyad részében lép a program N-be!

#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <random>

bool isPowerOfTen(unsigned long int input) {
    return
        input == 1L
        || input == 10L
        || input == 100L
        || input == 1000L
        || input == 10000L
        || input == 100000L
        || input == 1000000L
        || input == 10000000L
        || input == 100000000L
        || input == 1000000000L
        || input == 10000000000L
        || input == 100000000000L
        || input == 1000000000000L;
}

int main(int argc, char** argv)
{
    unsigned int N;
    if (argc > 1)
        N = atoi(argv[1]);
    else
        std::cin >> N;

    std::mt19937_64 engine(1000);
    std::uniform_int_distribution<int> distr(1, 6);

    long int stepIn = 0;                                   // how many times did I step into the desired N

    for (unsigned long int i = 0; i < 4294967294; ++i)     // i: number of games
    {
        unsigned long state = 0;                           // state of the game
        while (state < N)
            state += distr(engine);

        if (state == N)
            ++stepIn;

        if (isPowerOfTen(i))
        {
            int prec = int(log(sqrt(i)) / log(10)) + 3;
            std::cout.precision(prec);
            std::cout << stepIn / double(i) << " +- " << 1 / sqrt(i) << std::endl;

        }
    }

    return 0;
}
