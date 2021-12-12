# Calculator

- [Calculator](#calculator)
  - [How to use](#how-to-use)
  - [How the code works](#how-the-code-works)
  - [Code development](#code-development)

The aim is to create a webapp the can perform operations on the uploaded data in 5 different ways:

1. By calling numpy's vectorized (?) functions such as `array_for`, `array_map`, `fromiter` an `vectorize`
2. Doing similarly with pandas
3. Invoking Numba
4. call the already vectorized numpy functions after interpreting the operation
5. create a python module in cpp, and call that

The results would be shown to the users, as well as a short analysis on the performance.

## How to use

The program will be able to accept two mandatory inputs:

- an expression to be calculated, e.g. $$f(x,y) = sin(x \cdot y) + 0.2 \cdot \operatorname{pow}(y,2)$$
- A csv file including the variables as column headers and (the index column is optional)

| index |   x    |    y    |
| :---: | :----: | :-----: |
|   1   | 0.2121 | 0.5343  |
|   2   | 0.124  | 0.2121  |
|   3   | 0.8892 | 0.21222 |
|   4   | 0.2321 |  0.21   |

The return values are printed into a csv file and offered the user to download, but the main information is the calculation time.

## How the code works

As step, the syntax of the expression one can input has to be analyzed. It is similar the python's eval function with the difference is that I did it and have more control what happens inside. The syntax is then translated to numpy

## Code development

To understand the operation passed from the UI in a string, I needed to write an interpreter. It is also a good practice.

In the `initial_try.py`, I tried it without planning, without defining the syntax of the expression. Then in `ebnf.py`, I made the definition one by one, and implemented them. It turned out that the syntax structure got more complex then expected.

An EBNF definition of a nested expression is deduced as the followings.

A number is defined using EBNF as:

```EBNF
digit  ⇐ 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
uint   ⇐ digit {digit}
int    ⇐ [+|-] uint
number ⇐ int [.uint] [e|E int]
```

Without defining functions, we define expressions. It starts with either a number or a function (single or two arguments) name, and then may come an elementary operator, followed by another expression.

```EBNF
saopn  ⇐ | sin | cos | tan | arcsin | arccos | arctan | sinh | cosh | arctanh
taopn  ⇐ pow
eop    ⇐ + | - | * | /
expr   ⇐ ( number | ( saopn "(" expr ")" ) | ( taopn "(" expr , expr ")" ) ) { eop expr }
```

In this last example, the unquoted parenthesis represent grouping, and quoted parenthesis represent the parenthesis character.
