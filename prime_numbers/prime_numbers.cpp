// prime_numbers.cpp : This file contains the 'main' function. Program execution begins and ends there.
// keresd meg növekvõ sorrendben a prímszámokat

#include <iostream>
#include <vector>

using namespace std;

int main()
{
    vector<int> primes;

    for (int n = 2; ; n++)
    {
        bool isprime = true;
        for (int prime : primes)
        {
            if (n % prime == 0)
            {
                isprime = false;
                break;
            }
        }

        if (isprime)
        {
            primes.push_back(n);
            cout << n << endl;
        }
    }
    return 0;
}