// message_from_newspaper.cpp : This file contains the 'main' function. Program execution begins and ends there.
// egy nyomtatott üzenetet szeretnénk létrehozni egy újságpapírból olyan módon, hogy az üzenet betûit az újságpapírból szedjük ki úgy, hogy kivágjuk az újságpapírból és ráragasztjuk a megfelelõ sorrendben egy üres papírra. A szóköz kivéetlével az összes karaktert csak az újságpapírból szedhetjük. Szóközökbõl bárhányat készíthetünk az üzenetben. Annak érdekében, hogy meg tudjuk mondani elõre, hogy egy kívánt üzenet egy újságpapírból elõállítható-e, készítsünk egy függvényt, aminek két bemenete két string, ami az üzenetet és az újságpapír szövegét tartalmazza! A függvény adja vissza, hogy melyik az az elsõ karakter az üzenetben, amit nem állítható már elõ az újságból. Ha a teljes üzenet kirakható, akkor adjon vissza egy szóközt!

#include <iostream>
#include <map>
#include <string>

using namespace std;

char first_missing(string message, string newspaper)
{
    map<char, int> occ;
    for (char c : message)
    {
        if (c == ' ')
            continue;
        if (occ.find(c) != occ.end())
            occ[c]++;
        else
            occ[c] = 1;
    }

    for (char c : newspaper)
    {
        if (occ.find(c) != occ.end())
            occ[c] --;
    }

    for (char c : message)
        if (occ[c] > 0)
            return c;

    return ' ';
}

int main()
{
    string newspaper = "Hello World!";
    string message = "What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";

    cout << first_missing(message, newspaper) << endl;
}

