# Mi van itt?
Itt különféle apróbb python kódok vannak.

- [Mi van itt?](#mi-van-itt)
  - [prime.py](#primepy)
    - [nuitka telepítés](#nuitka-telepítés)
  - [fibonacci.py](#fibonaccipy)
  - [default_argument.py](#default_argumentpy)
  - [README.md](#readmemd)

## prime.py
Prímszámokat lehet generáltatni vele. Egy naív és egy kicsit jobb implementációt tartalmaz. Jó még sebességmérésre. Futtasd le `python prime.py` paranccsal, hogy lásd, mennyi ideig fut natívan pythonból. Majd fordítsd le exe-re a nuitkával a `python -m nuitka --mingw64 python.py` paranccsal először, majd futtasd az exe-t ˙.\prime.exe˙ PowerShellen.

Jellemző sebesség:
* natívan pythonnal: 2.5 s
* fordítva nuitkával: 1.8 s (30%-kal gyorsabb)

### nuitka telepítés
A nuitkát telepíteni kell, [kövesd a hivatalos weboldalt](https://github.com/Nuitka/Nuitka). Lehet, hogy [hibába ütközöl](https://github.com/Nuitka/Nuitka/issues/912), de a gcc-s windowsos telepítőt le tudod szedni és betenni a megfelelő helyre előbb utóbb.

## fibonacci.py
Fibonacci számokat generál. Nem olyan izgalmas.

## default_argument.py
Ha a default argument mutable, az néha meglepő eredményekre vezethet.

## README.md
Ez a leírás maga.