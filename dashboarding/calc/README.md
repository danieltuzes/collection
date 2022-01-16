# The calculator python project

A python example with a HTML interface on how to process strings representing an operation.

- [The calculator python project](#the-calculator-python-project)
  - [How to use](#how-to-use)
  - [How the code works](#how-the-code-works)
  - [Code development](#code-development)

The aim is to create a webapp the can perform operations on data provided by the user,
and shows the result to the user and offer it for downloading.

## How to use

The program is be able to accept two mandatory inputs:

1. an expression to be calculated, e.g.
   1. a $\mathbb{R} \to \mathbb{R}$ function, such as $f(x) = x^2$
   2. an ${\mathbb{R}^N} \to \mathbb{R}$ function, e.g.  using $N=2$: $f(x,y) = \sin(x \cdot y) + 0.2 \cdot \operatorname{pow}(y,2)$
2. Input data, provided as
   1. list of individual values
   2. a given number of random values in the range $\left[ {0,1} \right)$
   3. a csv file including the variables as column headers (the index column is optional)

| index |   x    |    y    |
| :---: | :----: | :-----: |
|   1   | 0.2121 | 0.5343  |
|   2   | 0.124  | 0.2121  |
|   3   | 0.8892 | 0.21222 |
|   4   | 0.2321 |  0.21   |

The input values are put into a pandas table structure, the function is evaluated on the columns and the result is appended to the table.
The first few lines of this table are shown to the user,
and the full table is offered for download.

## How the code works

The input data is analyzed, and the column headers as variables are identified.

Then the syntax of the expression has to be analyzed. It is similar the python's eval function with the difference
that I wrote it myself therefore I have more control what happens inside. The syntax is then translated to numpy's
vectorized operations.

## Code development

To understand the operation passed from the UI in a string, I needed to write an interpreter. It is also a good practice.

In the `initial_try.py`, I tried it without planning, without defining the syntax of the expression. Then in `ebnf.py`, I made the definition one by one, and implemented them. It turned out that the syntax structure got more complex then expected.

An EBNF definition of a nested expression is deduced as the followings.

A number is defined using EBNF as:

```EBNF
digit  = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
uint   = digit {digit};
int    = ["+"|"-"] uint;
number = int ["." uint] ["e"|"E" int];
```

Without defining functions, we define expressions. It starts with either a number or a function (single or two arguments) name, and then may come an elementary operator, followed by another expression.

```EBNF
saopn  = | "sin" | "cos" | "tan" | "arcsin" | "arccos" | "arctan" | "sinh" | "cosh" | "arctanh";
taopn  = "pow";
eop    = "+" | "-" | "*" | "/";
expr   = ( number | ( saopn "(" expr ")" ) | ( taopn "(" expr , expr ")" ) ) { eop expr };
```

In this last example, the unquoted parenthesis represent grouping, and quoted parenthesis represent the parenthesis character.

Then I added the ability to handle a single variable (containing an numpy array of values),
then the ability to handle multiple variables.
I also created the webapp in parallel.

In the end I realized that there are [many aspects of efficiency](https://stackoverflow.com/questions/35215161/most-efficient-way-to-map-function-over-numpy-array), and it is better to dig deeper into this topic
once the specific problem arises.

Content of the source file:
