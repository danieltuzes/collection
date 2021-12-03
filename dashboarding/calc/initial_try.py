"""Interpret math operations on numbers.
Doesn't handle exponential notation, already quite lengthy
and feels ad-hoc."""

import math
import sys
from typing import Union

op_1arg = {"sin": math.sin,
           "cos": math.cos,
           "log": math.log}

op_2arg = {"pow": math.pow}

DIGITS = "0123456789"


EXPR1 = "1+2 *4*  (16+3*5+12*sin(12+8*3+15))+(11+4*7+13)"
EXPR2 = "-12+ 8*3  +15"
EXPR3 = "10*2*12/15/-44"


def calc(expr: str) -> str:
    """Calculate expression with ()s"""
    r_par = expr.find(")")
    l_par = expr[:r_par].rfind("(")
    if bool(l_par) != bool(r_par):
        raise ValueError("The number of left and right parenthesis must be "
                         f"the same. It doesn't hold for {expr}")

    while not l_par == r_par == -1:
        print("Expression:", expr)
        inner = expr[l_par+1:r_par]
        print("Most inner part:", inner)
        op_found = False
        if l_par+1-4 > -1:
            op_name = expr[l_par+1-4:l_par]
            if op_name in op_1arg:
                inner = str(op_1arg[op_name](num(inner)))
                l_par -= 3
                op_found = True
            elif op_name in op_2arg:
                args = inner.split(",")
                inner = str(op_2arg[op_name](num(args[0]), num(args[1])))
                l_par -= 3
                op_found = True
        if not op_found:
            inner = evaluate(inner)
        expr = expr[:l_par] + inner + expr[r_par+1:]
        expr = expr.replace("--", "+")
        expr = expr.replace("*+", "*")
        expr = expr.replace("/+", "/")
        r_par = expr.find(")")
        l_par = expr[:r_par].rfind("(")
        if bool(l_par) != bool(r_par):
            raise ValueError("Number of left and right parenthesis must be "
                             f"the same. It doesn't hold for {expr}")

    return evaluate(expr)


def evaluate(expr: str) -> str:
    "Evaluates an expression without ()s."
    if not (expr[0] == "-" or DIGITS.find(expr[0])):
        raise ValueError(f"Expression cannot start with {expr}")

    mul_l = expr.find("*")
    div_l = expr.find("/")

    while not mul_l == div_l == -1:
        if div_l > mul_l > 0 or div_l == -1:
            l_o_start = left_o(expr, mul_l)
            l_o = num(expr[l_o_start:mul_l])
            r_o_end = right_o(expr, mul_l)
            r_o = num(expr[mul_l+1:r_o_end+1])
            res = l_o * r_o

        if mul_l > div_l > 0 or mul_l == -1:
            l_o_start = left_o(expr, div_l)
            l_o = num(expr[l_o_start:div_l])
            r_o_end = right_o(expr, div_l)
            r_o = num(expr[div_l+1:r_o_end+1])
            res = l_o / r_o

        expr = expr[:l_o_start] + str(res) + expr[r_o_end+1:]
        print(expr)

        mul_l = expr.find("*")
        div_l = expr.find("/")

    add_l = expr.find("+")
    sub_l = expr[1:].find("-")
    if sub_l != -1:
        sub_l += 1

    while not add_l == sub_l == -1:
        if sub_l > add_l > 0 or sub_l == -1:
            l_o_start = left_o(expr, add_l)
            l_o = num(expr[l_o_start:add_l])
            r_o_end = right_o(expr, add_l)
            r_o = num(expr[add_l+1:r_o_end+1])
            res = l_o + r_o

        if add_l > sub_l > 0 or add_l == -1:
            l_o_start = left_o(expr, sub_l)
            l_o = num(expr[l_o_start:sub_l])
            r_o_end = right_o(expr, sub_l)
            r_o = num(expr[sub_l+1:r_o_end+1])
            res = l_o - r_o

        expr = expr[:l_o_start] + str(res) + expr[r_o_end+1:]
        print(expr)

        add_l = expr.find("+")
        sub_l = expr[1:].find("-")
        if sub_l != -1:
            sub_l += 1

    return expr


def num(representation: str) -> Union[int, float]:
    """Returns the value of string as int or float."""
    try:
        return int(representation)
    except ValueError:
        return float(representation)


def left_o(expr: str, pos: int) -> int:
    """Find the starting point of left operand from pos."""
    r_plus = expr[:pos].rfind("+")  # the last +
    r_dash = expr[:pos].rfind("-")  # the last -
    if r_dash+1 == r_plus:
        raise ValueError(f"The sign + in {expr} is mis-placed.")
    if r_plus+1 == r_dash:
        return r_dash
    if r_dash > r_plus:
        return r_dash+1
    return r_plus + 1


def right_o(expr: str, pos: int) -> int:
    """Find the end point of right operand from pos."""
    l_plus = expr[pos+1:].find("+")  # the first +
    l_dash = expr[pos+2:].find("-")  # the first -
    if l_dash+1 == l_plus:
        raise ValueError(f"The sign + in {expr} is mis-placed.")

    l_mul = expr[pos+1:].find("*")  # the first *
    l_div = expr[pos+1:].find("/")  # the first /

    op_list = [l_plus, l_dash, l_mul, l_div]
    op_list = [len(expr)-pos if x < 0 else x for x in op_list]
    first = sorted(op_list)[0]
    if first == sorted(op_list)[3]:  # all -1
        return first+pos
    if first <= l_dash or l_dash == -1:
        return first+pos
    else:
        return l_dash + pos + 1


def main(input_expr: str) -> None:
    """C-style main."""
    print(input_expr)
    m_expr = input_expr.replace(" ", "")
    print(calc(m_expr))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(EXPR1)
