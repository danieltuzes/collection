"""Expression interpreter. Interprets +-*/, sin, cos, sinh, cosh, pow. Example:

1-pow(1-pow(cos(1e-3),2),0.5)*1e3"""

import math
from typing import List, Union, Tuple

DIGITS = "0123456789"
FUNC_1 = ["", "sin", "cos", "tan", "arcsin",
          "arccos", "arctan", "sinh", "cosh", "arctanh"]
FUNC_2 = ["pow"]
FUNC_C = "".join([*FUNC_1, *FUNC_2])  # str of possible chars for a func
PARENT = 0


def consume_number(seq: str, pos: int = 0) -> Tuple[Union[int, float], int]:
    """Read in a number from seq starting at pos.
    May finish before stop, and that position is returned together with the value.

    If it is not a number, raises a ValueError."""
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


def consume_expr(seq: str,
                 pos: int = 0,
                 until: str = "") -> Tuple[Union[float, int], int]:
    """Consume a single value starting from pos."""
    values: List[Union[float, int]] = []
    ops = {1: [], 2: [], 3: [], 4: []}
    i: int = 0

    value, pos = consume_value(seq, pos)
    values.append(value)

    while pos < len(seq) and (not until or (seq[pos] != until)):
        operator, pos = consume_op(seq, pos)
        ops[operator].append(i)
        i += 1
        value, pos = consume_value(seq, pos)
        values.append(value)

    while ops[3] or ops[4]:
        if ((ops[3] and ops[4]) and (ops[3][0] < ops[4][0])) or (ops[3] and not ops[4]):
            values[ops[3][0]+1] = values[ops[3][0]] * values[ops[3][0]+1]
            ops[3].pop(0)
        else:
            values[ops[4][0]+1] = values[ops[4][0]] / values[ops[4][0]+1]
            ops[4].pop(0)

    while ops[1] or ops[2]:
        if ((ops[1] and ops[2]) and (ops[1][0] < ops[2][0])) or (ops[1] and not ops[2]):
            lhv = values[ops[1][0]]
            ops[1].pop(0)
            rhv_i = min([*ops[1], *ops[2], len(values)-1])
            values[rhv_i] = lhv + values[rhv_i]
        else:
            lhv = values[ops[2][0]]
            ops[2].pop(0)
            rhv_i = min([*ops[1], *ops[2], len(values)-1])
            values[rhv_i] = lhv - values[rhv_i]
    return values[-1], pos


def consume_value(seq: str, pos: int) -> Tuple[Union[float, int], int]:
    """Reads in a function or number values."""
    start = pos
    while seq[pos] in FUNC_C:
        pos += 1
    if pos > start or seq[start] == "(":
        func_name = seq[start:pos]
        pos = consume_parent(seq, pos)
        if func_name in FUNC_1:
            num, pos = consume_expr(seq, pos, ")")
            pos = consume_parent(seq, pos)
            if func_name == "":
                value = num
            elif func_name == "sin":
                value = math.sin(num)
            elif func_name == "cos":
                value = math.cos(num)
            elif func_name == "sinh":
                value = math.sinh(num)
            elif func_name == "cosh":
                value = math.cosh(num)
        elif func_name in FUNC_2:
            num_1, pos = consume_expr(seq, pos, ",")
            pos = consume_comma(seq, pos)
            num_2, pos = consume_expr(seq, pos, ")")
            pos = consume_parent(seq, pos)
            if func_name == "pow":
                value = math.pow(num_1, num_2)
        else:
            raise ValueError(f"{func_name} is not an function name in seq")
    else:
        value, pos = consume_number(seq, pos)

    return value, pos


def consume_parent(seq: str, pos: int) -> int:
    """Raise ValueException if cannot consume the upcoming ( or ), return pos+1 otherwise"""
    global PARENT  # pylint: disable = global-statement
    if PARENT and (seq[pos] not in "()"):
        raise ValueError(f"{seq} at position {pos} is not a parenthesis")
    if not PARENT and (seq[pos] != "("):
        raise ValueError(f"{seq} at position {pos} is not a '(' char")
    if seq[pos] == "(":
        PARENT += 1
    else:
        PARENT -= 1
    return pos+1


def consume_comma(seq: str, pos: int) -> int:
    "Raise ValueException if cannot consume a ',' return pos+1 otherwise"
    if seq[pos] != ",":
        raise ValueError(f"{seq} at position {pos} is not a ',' char")
    return pos+1


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
        f"Expression {seq} at {pos} is {seq[pos]},"
        " which is not an elementary operator.")


if __name__ == "__main__":
    while True:
        my_text = input()
        try:
            print(consume_expr(my_text, 0)[0])
        except ValueError as error:
            print(f"It is not a valid expression: {error}")
        except Exception as error:
            print(f"It is not a valid expression: {error}")
