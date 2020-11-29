// sandbox.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <chrono>

using namespace std;

#include <boost/random/ranlux.hpp>
#include <boost/random/mersenne_twister.hpp>          // random number generator
#include <boost/random/uniform_real_distribution.hpp> // uniform distribution generator



int main()
{

    int n;
    cin >> n;

    vector<int> primes;
    for (int i = 2; i < n; ++i)
    {
        bool isprime = true;
        for (auto prime : primes)
        {
            if (i % prime == 0)
            {
                isprime = false;
                break;
            }
        }
        if (isprime)
            primes.push_back(i);
    }

    for (auto prime : primes)
        cout << prime << "\n";
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
