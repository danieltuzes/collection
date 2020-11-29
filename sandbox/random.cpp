// sandbox.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <chrono>

using namespace std;

#include <boost/random/mersenne_twister.hpp>          // random number generator
#include <boost/random/uniform_real_distribution.hpp> // uniform distribution generator

int main()
{
    boost::random::mt19937 engine(1000);
    uniform_real_distribution<float> u(0, 1);
    double ub = 1e-9;                           // the upper boundary for the correlation integral
    size_t l1cycle = 1'400;                     // inner loop, doesn't stop
    size_t chcycle = 10'000;                    // after this many loops, checks for STOP.txt
    size_t c = 0;                               // whole loop cycle count
    size_t pair_c = 0;                          // whole loop cycle count
    engine.discard(1e11);

    auto begin = std::chrono::high_resolution_clock::now();

    for (; c < SIZE_MAX / l1cycle / chcycle && pair_c < SIZE_MAX - l1cycle * chcycle; ++c)
    {
        for (int n = 0; n < chcycle; ++n)
        {
            vector<double> history;             // stores the values
            history.reserve(l1cycle);           // L1 cache size must be a bit bigger to store all the values
            for (int i = 0; i < l1cycle; ++i)   // fill up history with random numbers
            {
                double rnd = u(engine);
                for (int j = 0; j < i; ++j)     // look up all the previous elements
                {
                    pair_c++;
                    double d = fabs(rnd - history[j]);
                    if (d < ub)                 // if the distance is in the region of interest
                        cout << d << "\n";
                }
                history.push_back(rnd);
            }
        }

        ifstream STOP("STOP.txt");
        if (STOP)
            break;

        cout.flush();
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::nanoseconds>(end - begin).count();
    cout << "# total number of pairs investigated: " << pair_c << endl;
    cout << "# time per pair: " << double(duration) / pair_c << endl;


    return 0;
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
