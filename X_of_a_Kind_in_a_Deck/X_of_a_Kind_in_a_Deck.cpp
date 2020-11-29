// X_of_a_Kind_in_a_Deck.cpp : This file contains the 'main' function. Program execution begins and ends there.
/* In a deck of cards, each card has an integer written on it.

Return true ifand only if you can choose X >= 2 such that it is possible to split the entire deck into 1 or more groups of cards, where:

Each group has exactly X cards. All the cards in each group have the same integer.



Example 1:

Input: [1, 2, 3, 4, 4, 3, 2, 1]
Output : true
Explanation : Possible partition[1, 1], [2, 2], [3, 3], [4, 4]

Example 2 :

    Input : [1, 1, 1, 2, 2, 2, 3, 3]
    Output : false
    Explanation : No possible partition.

    Example 3 :

    Input : [1]
    Output : false
    Explanation : No possible partition.

    Example 4 :

    Input : [1, 1]
    Output : true
    Explanation : Possible partition[1, 1]

    Example 5 :

    Input : [1, 1, 2, 2, 2, 2]
    Output : true
    Explanation : Possible partition[1, 1], [2, 2], [2, 2]


    Note :

    1 <= deck.length <= 10000
    0 <= deck[i] < 10000
 */

#include <iostream>
#include <map>
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:

    static vector<int> primes;

    static bool hasGroupsSizeX(vector<int>& deck)
    {
        if (primes.empty())
            primes.push_back(2);

        map<int, int> occurance;
        for (auto val : deck)
        {
            if (occurance.find(val) != occurance.end())
                occurance[val]++;
            else
                occurance[val] = 1;
        }

        int LNKO_in_occ = occurance.begin()->second;

        for (auto val : occurance)
            LNKO_in_occ = LNKO(LNKO_in_occ, val.second);

        if (LNKO_in_occ > 1)
            return true;
        return false;
    }

    static bool hasKnownDivisor(int n)
    {
        for (auto prime : primes)
        {
            if (n % prime == 0)
                return true;
        }
        return false;
    }

    static vector<int> primeDivisors(int n) // returns the list of prime numbers of which product returns the number n
    {
        vector<int> ret;

        for (auto prime : primes)
        {
            while (n % prime == 0)
            {
                ret.push_back(prime);
                n /= prime;
            }
        }

        while (primes.back() < sqrt(n))
        {
            int newPrime = primes.back() + 1;               // the nominated new prime number
            for (; hasKnownDivisor(newPrime); ++newPrime);  // it is not a prime if it has a divisor that is smaller than that value
            primes.push_back(newPrime);                     // newPrime is a prime now, for sure
            while (n % newPrime == 0)                       // check if the new prime divides n and how many time
            {
                ret.push_back(newPrime);                    // remember how many times it divides
                n /= newPrime;                              // n will be factorised
            }
        }

        if (ret.empty())
        {
            primes.push_back(n);
            ret.push_back(n);
        }

        return ret;
    }

    static vector<int> LNKOfactors(int a, int b)    // largest common divisor
    {
        vector<int> aFactor = primeDivisors(a);
        vector<int> bFactor = primeDivisors(b);

        size_t LNKOsize = min(aFactor.size(), bFactor.size());
        vector<int> ret(LNKOsize);

        auto endIt = set_intersection(aFactor.begin(), aFactor.end(), bFactor.begin(), bFactor.end(), ret.begin());
        ret.resize(endIt - ret.begin());

        if (ret.empty())
            ret.push_back(1);

        return ret;
    }

    static int LNKO(int a, int b)
    {
        if (a == 1 || b == 1)
            return 1;
        
        int ret = 1;
        
        for (auto prime : LNKOfactors(a, b))
            ret *= prime;
        return ret;
    }
};

vector<int> Solution::primes = { 2 };

int main()
{
    //vector<int> input = { 1,2,3,4,4,3,2,1 };
    //vector<int> input = { 1,1,1,2,2,2,3,3 };
    //vector<int> input = { 1 };
    //vector<int> input = { 1,1};
    //vector<int> input = { 1,1,2,2,2,2};
    //vector<int> input = { 1,1,1,2,2,2,2,2,2};
    vector<int> input = { 1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,3,3};

    if (Solution::hasGroupsSizeX(input))
        cout << "true";
    else
        cout << "false";
    return 0;
    for (int i = 2; i < 100; ++i)
        for (int j = 2; j < 100; ++j)
        {
            cout << "LNKO(" << i << ";" << j << ")\t= LNKO(p(";
            for (auto prime : Solution::primeDivisors(i))
                cout << prime << ";";
            cout << ");p(";
            for (auto prime : Solution::primeDivisors(j))
                cout << prime << ";";
            cout << ")\t= p(";
            for (auto prime : Solution::LNKOfactors(i, j))
                cout << prime << ";";
            cout << ")" << endl;
        }
}