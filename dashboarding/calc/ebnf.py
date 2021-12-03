"""Nested expressions of numbers with the
elementary operators and 1 or 2 argumental functions.

A number is defined using EBNF as:

digit  ⇐ 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
uint   ⇐ digit {digit}
int    ⇐ [+|-] uint
number ⇐ int [.uint] [e|E int]

Elementary expression consists of
numbers and elementary operations between them:

eop    ⇐ + | - | * | /
eexpr  ⇐ number {eop number}

Single argument functions are
operations on numbers
between parenthesis denoted by their name.
Function without name is pure parenthesis

saopn  ⇐ | sin | cos | tan | arcsin | arccos | arctan | sinh | cosh | arctanh
sfunc  ⇐ saopn ( eexpr )

Two argument functions are
operations on elementary expressions
and on another argument, separated by comma,
between parenthesis, denoted by their name-

taopn ⇐ pow
tfunc ⇐ taopn ( eexpr , eexpr)

value ⇐ sfunc | tfunc | eexpr

e_value = value {eop value}

nested_expr ⇐ e_value | saopn ( nested_expr ) | tfunc ( nested_expr , nested_expr )
"""

import math
from typing import Union, Tuple

DIGITS = "0123456789"
FUNC_1 = ["sin", "cos", "tan", "arcsin",
          "arccos", "arctan", "sinh", "cosh", "arctanh"]
FUNC_2 = ["pow"]
FUNC_C = "".join([*FUNC_1, *FUNC_2])  # str of possible chars for a func
PARENT = 0


def consume_number(seq: str, pos: int = 0) -> Tuple[Union[int, float], int]:
    """Read in a number from seq starting at iter.

    Returns the end of the number and its value. If it is not a number,
    raises a ValueError."""
    num_sign, pos = consume_sign(seq, pos)
    integral, pos = consume_uint(seq, pos)

    fractional = 0
    if pos < len(seq) and seq[pos] == ".":
        fractional, pos = consume_frac(seq, pos+1)

    absval = integral + fractional

    if pos < len(seq) and seq[pos] in "eE":
        exp_sign, pos = consume_sign(seq, pos+1)
        exponent, pos = consume_uint(seq, pos)
        absval *= 10**(exp_sign*exponent)

    return num_sign * absval, pos


def consume_sign(seq: str, pos: int) -> Tuple[int, int]:
    """Returns
    - +1, iter+1 if it is +
    - -1, iter+1 if it is -
    - +1, iter otherwise"""
    if seq[pos] == "-":
        return -1, pos+1
    if seq[pos] == "+":
        return 1, pos+1
    return 1, pos


def consume_uint(seq: str, pos: int) -> Tuple[int, int]:
    """Read in an integer, and return the value the end of it."""
    start = pos
    while pos < len(seq) and seq[pos] in DIGITS:
        pos += 1
    return int(seq[start:pos]), pos


def consume_frac(seq: str, pos: int) -> Tuple[float, int]:
    """Read in a fractional, return the value and the end of it."""
    start = pos
    while pos < len(seq) and seq[pos] in DIGITS:
        pos += 1
    return float("0."+seq[start:pos]), pos


def consume_eexpr(seq: str, pos: int, tillc="") -> Tuple[Union[float, int], int]:
    """Execute the 4 elementary operation used without parenthesis.
    tillc: till closing character"""
    num, pos = consume_number(seq, pos)
    nums = [num]
    ops = {1: [], 2: [], 3: [], 4: []}
    i: int = 0  # index of the operator
    while pos < len(seq) and (not tillc or (seq[pos] != tillc)):
        operator, pos = consume_op(seq, pos)
        ops[operator].append(i)
        i += 1

        nextnum, pos = consume_number(seq, pos)
        nums.append(nextnum)

    while ops[3] or ops[4]:
        if ((ops[3] and ops[4]) and (ops[3][0] < ops[4][0])) or (ops[3] and not ops[4]):
            nums[ops[3][0]+1] = nums[ops[3][0]] * nums[ops[3][0]+1]
            ops[3].pop(0)
        else:
            nums[ops[4][0]+1] = nums[ops[4][0]] / nums[ops[4][0]+1]
            ops[4].pop(0)

    while ops[1] or ops[2]:
        if ((ops[1] and ops[2]) and (ops[1][0] < ops[2][0])) or (ops[1] and not ops[2]):
            lhv = nums[ops[1][0]]
            ops[1].pop(0)
            rhv_i = min([*ops[1], *ops[2], len(nums)-1])
            nums[rhv_i] = lhv + nums[rhv_i]
        else:
            lhv = nums[ops[2][0]]
            ops[2].pop(0)
            rhv_i = min([*ops[1], *ops[2], len(nums)-1])
            nums[rhv_i] = lhv - nums[rhv_i]
    return nums[-1], pos


def consume_op(seq: str, pos: int) -> Tuple[int, int]:
    """Returns the operator and pos+1 if found. 0: not found, 1: +, 2: -, 3: *, 4: /"""
    if seq[pos] == "+":
        return 1, pos+1
    if seq[pos] == "-":
        return 2, pos+1
    if seq[pos] == "*":
        return 3, pos+1
    if seq[pos] == "/":
        return 4, pos+1
    raise ValueError(
        "Expression %s at %d is not an elementary operator." % (seq, pos))


def consume_value(seq: str, pos: int) -> Tuple[int, int]:
    """Read in a number or a function having 1 or 2 arguments."""
    start = pos
    while seq[pos] in FUNC_C:
        pos += 1
    if pos > start or seq[start] == "(":
        func_name = seq[start:pos]
        pos = consume_parent(seq, pos)
        if func_name in FUNC_1:
            num, pos = consume_eexpr(seq, pos, ")")
            pos = consume_parent(seq, pos)
            if func_name == "":
                value = num
            elif func_name == "sin":
                value = math.sin(num)
        elif func_name in FUNC_2:
            num_1, pos = consume_eexpr(seq, pos, ",")
            pos = consume_comma(seq, pos)
            num_2, pos = consume_eexpr(seq, pos, ")")
            pos = consume_parent(seq, pos)
            if func_name == "pow":
                value = math.pow(num_1, num_2)
        else:
            raise ValueError("%s is not an function name in seq" % func_name)
    else:
        value, pos = consume_eexpr(seq, pos)
    return value, pos


def consume_parent(seq: str, pos: int) -> int:
    """Raise ValueException if cannot consume the upcoming ( or ), return pos+1 otherwise"""
    global PARENT
    if PARENT and (seq[pos] not in "()"):
        raise ValueError("%s at position %d is not a parenthesis" % (seq, pos))
    if not PARENT and (seq[pos] != "("):
        raise ValueError("%s at position %d is not a '(' char" % (seq, pos))
    if seq[pos] == "(":
        PARENT += 1
    else:
        PARENT -= 1
    return pos+1


def consume_comma(seq: str, pos: int) -> int:
    "Raise ValueException if cannot consume a ',' return pos+1 otherwise"
    if seq[pos] != ",":
        raise ValueError("%s at position %d is not a ',' char" % (seq, pos))
    return pos+1


if __name__ == "__main__":
    while True:
        my_text = input()
        try:
            print(consume_value(my_text, 0)[0])
        except ValueError as error:
            print("It is not a valid expression.")
            raise error
