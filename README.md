# collection
Érdekes feladványok, gyakorlások és homokozó

Többféle, egyenként apró programot vagy szkriptet gyűjtötem itt össze. Némelyek állásinterjúkon kerültek elő, másokat saját célra kellett előállítanom.

**Tartalomjegyzék**
- [collection](#collection)
- [bash szkriptek](#bash-szkriptek)
- [C++ programocskák](#c-programocskák)
- [python szkriptek](#python-szkriptek)

# bash szkriptek
Néhány bash szkript, amikkel legalább pár órát elszöszöltem, így emlékezni fogok rájuk később, hogy csináltam ilyet is. Így viszont meg is tudom majd találni, és kikeresni 1-1 részt, ha kell.
* [szólj, ha lejárt](do_if_finished): Ha lefutnak bizonyos parancsok, akkor e-mailt küld róla és végrehajt egy parancsot is.

# C++ programocskák

* **dict_to_n**: Írj egy numerikus szimulációt, ami a következő játékot játsza. Az 0-s mezőből indulsz és annyit lépsz előre, ahanyast dobsz egy dobókockával. A kérdés, hogy az összes játékhoz képest a játékok mekkora részében lépsz egy előre megadott mezőbe? Legyen ennek az értéke N! Ennek segítségével megadható, hogy empirikusan mekkora a valószínűsége, hogy egy adott mezőbe lépsz. A program vegye az első és egyetlen hívási argumentumot az N értékének, vagy ha nincs megadva hívási paraméterként, akkor kérje be a standard inputról. Majd írja ki, hogy 10, 100, ... stb játékra vetítve az esetek hanyad részében lép a program N-be!
* **safety_joe**: Az alábbi játékot játszunk egy 32 kártyás francia kártyával, amiben 16 fekete és 16 piros színű kártya van. Egy körben a kártyaosztó leemel a megkevert kártyapakliból 1 lapot, és meg kell tippelnem a színét. A tétet, amit felteszek a tippem helyességére, én választom meg minden körben. A tét megtétele után a kártyaosztó megmutatja a kártyát, majd kivonja a játékból. Ha eltaláltam a színét, akkor a tétem dupláját kapom meg. Ha vesztek, akkor a tétemet elbukom. A játékot addig játszuk, amíg az összes kártyát ki nem vonta az osztó a játékból, és a feladatom maximalizálni a pénzemet a játék végére a legszerencsétlenebb kártyasorrend esetére is. (Tehát nem a nyeremény várható értéke érdekel, hanem hogy mennyi az a pénz, amit legalább nyerhetek.)

    Programozd le a nyerő stratégiát, azaz ami kiszámolja, hogy adott helyzetben mi a nyerő tétösszeg az aktuális lépésnél, és hogy mennyi a minimálisan várható nyeremény!
* **X_of_a_Kind_in_a_Deck**:In a deck of cards, each card has an integer written on it.

    Return true ifand only if you can choose X >= 2 such that it is possible to split the entire deck into 1 or more groups of cards, where:

    Each group has exactly X cards. All the cards in each group have the same integer.
* **prime_numbers**: keresd meg növekvő sorrendben a prímszámokat
* **message_from_newspaper**: egy nyomtatott üzenetet szeretnénk létrehozni egy újságpapírból olyan módon, hogy az üzenet betűit az újságpapírból szedjük ki úgy, hogy kivágjuk az újságpapírból és ráragasztjuk a megfelelő sorrendben egy üres papírra. A szóköz kivéetlével az összes karaktert csak az újságpapírból szedhetjük. Szóközökből bárhányat készíthetünk az üzenetben. Annak érdekében, hogy meg tudjuk mondani előre, hogy egy kívánt üzenet egy újságpapírból előállítható-e, készítsünk egy függvényt, aminek két bemenete két string, ami az üzenetet és az újságpapír szövegét tartalmazza! A függvény adja vissza, hogy melyik az az első karakter az üzenetben, amit nem állítható már elő az újságból. Ha a teljes üzenet kirakható, akkor adjon vissza egy szóközt!

# python szkriptek

* **cheap_flights**: Check the cheapest flight prices via skyscanner's API and send an email if prices are changed.