// safety_joe.cpp : This file contains the 'main' function. Program execution begins and ends there.
// Az alábbi játékot játszunk egy 32 kártyás francia kártyával, amiben 16 fekete és 16 piros színû kártya van. Egy körben a kártyaosztó leemel a megkevert kártyapakliból 1 lapot, és meg kell tippelnem a színét. A tétet, amit felteszek a tippem helyességére, én választom meg minden körben. A tét megtétele után a kártyaosztó megmutatja a kártyát, majd kivonja a játékból. Ha eltaláltam a színét, akkor a tétem dupláját kapom meg. Ha vesztek, akkor a tétemet elbukom. A játékot addig játszuk, amíg az összes kártyát ki nem vonta az osztó a játékból, és a feladatom maximalizálni a pénzemet a játék végére a legszerencsétlenebb kártyasorrend esetére is. (Tehát nem a nyeremény várható értéke érdekel, hanem hogy mennyi az a pénz, amit legalább nyerhetek.)

// Programozd le a nyerõ stratégiát, azaz ami kiszámolja, hogy adott helyzetben mi a nyerõ tétösszeg az aktuális lépésnél, és hogy mennyi a minimálisan várható nyeremény!

#include <iostream>
#include <map>
#include <utility>

std::pair<double, double> calc_bet_profit_factor(int r, int b)   // optimal bet and profit factor
{

    if (r == 1 && b == 1)
        return std::pair<double, double>(0, 2);

    if (b == 0)
        return std::pair<double, double>(1, pow(2,r));

    if (r == b)
        return std::pair<double, double>(0, calc_bet_profit_factor(r, b - 1).second);


    double c_b = calc_bet_profit_factor(r, b - 1).second;
    double c_r = calc_bet_profit_factor(r - 1, b).second;

    double bet = (c_b - c_r) / (c_b + c_r);
    double profit = (1 - bet) * c_b;
    return std::pair<double, double>(bet, profit);
}

int main()
{
    std::cout << "Number of black cards: ";
    int r = 0;
    std::cin >> r;

    std::cout << "Number of black cards: ";
    int b = 0;
    std::cin >> b;

    if (r + b > 32 || r > 16 || b > 16)
        std::cerr << "Card number error." << std::endl;

    if (r < b)  // later wlog we suppose r > b
        std::swap(r, b);

    std::pair<double, double> optimal_bet_profit = calc_bet_profit_factor(r, b);
    std::cout << "bet:\t" << optimal_bet_profit.first << std::endl;
    std::cout << "profit:\t" << optimal_bet_profit.second << std::endl;

}