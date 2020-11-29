// safety_joe.cpp : This file contains the 'main' function. Program execution begins and ends there.
// Az al�bbi j�t�kot j�tszunk egy 32 k�rty�s francia k�rty�val, amiben 16 fekete �s 16 piros sz�n� k�rtya van. Egy k�rben a k�rtyaoszt� leemel a megkevert k�rtyapaklib�l 1 lapot, �s meg kell tippelnem a sz�n�t. A t�tet, amit felteszek a tippem helyess�g�re, �n v�lasztom meg minden k�rben. A t�t megt�tele ut�n a k�rtyaoszt� megmutatja a k�rty�t, majd kivonja a j�t�kb�l. Ha eltal�ltam a sz�n�t, akkor a t�tem dupl�j�t kapom meg. Ha vesztek, akkor a t�temet elbukom. A j�t�kot addig j�tszuk, am�g az �sszes k�rty�t ki nem vonta az oszt� a j�t�kb�l, �s a feladatom maximaliz�lni a p�nzemet a j�t�k v�g�re a legszerencs�tlenebb k�rtyasorrend eset�re is. (Teh�t nem a nyerem�ny v�rhat� �rt�ke �rdekel, hanem hogy mennyi az a p�nz, amit legal�bb nyerhetek.)

// Programozd le a nyer� strat�gi�t, azaz ami kisz�molja, hogy adott helyzetben mi a nyer� t�t�sszeg az aktu�lis l�p�sn�l, �s hogy mennyi a minim�lisan v�rhat� nyerem�ny!

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