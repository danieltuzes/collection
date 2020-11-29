// message_from_newspaper.cpp : This file contains the 'main' function. Program execution begins and ends there.
// egy nyomtatott �zenetet szeretn�nk l�trehozni egy �js�gpap�rb�l olyan m�don, hogy az �zenet bet�it az �js�gpap�rb�l szedj�k ki �gy, hogy kiv�gjuk az �js�gpap�rb�l �s r�ragasztjuk a megfelel� sorrendben egy �res pap�rra. A sz�k�z kiv�etl�vel az �sszes karaktert csak az �js�gpap�rb�l szedhetj�k. Sz�k�z�kb�l b�rh�nyat k�sz�thet�nk az �zenetben. Annak �rdek�ben, hogy meg tudjuk mondani el�re, hogy egy k�v�nt �zenet egy �js�gpap�rb�l el��ll�that�-e, k�sz�ts�nk egy f�ggv�nyt, aminek k�t bemenete k�t string, ami az �zenetet �s az �js�gpap�r sz�veg�t tartalmazza! A f�ggv�ny adja vissza, hogy melyik az az els� karakter az �zenetben, amit nem �ll�that� m�r el� az �js�gb�l. Ha a teljes �zenet kirakhat�, akkor adjon vissza egy sz�k�zt!

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

