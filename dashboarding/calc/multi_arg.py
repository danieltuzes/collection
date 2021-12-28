"""Apply a multiple argument function on a numpy array.

The array is a numpy ndarray of random values in [0,1), denoted by x,
and the function definition has to be given. As an example,
one can give the right hand side of
$$f(x) = sin(2*3.14159*x)/x$$

Similar to ebnf_full, but this can accept a function argument,
which is an array and can be arbitrary long.
"""

import string
import math
from typing import List, Union, Tuple
import numpy as np

Value = Union[float, int, np.ndarray]

DIGITS = "0123456789"
FUNC_S = ["sin", "cos", "tan", "arcsin",
          "arccos", "arctan", "sinh", "cosh", "arctanh"]
FUNC_1 = ["", *FUNC_S]
FUNC_2 = ["pow"]
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
                 arr: dict[str, np.ndarray],
                 pos: int = 0,
                 until: str = "") -> Tuple[Value, int]:
    """Consume a single value starting from pos."""
    values: List[Value] = []
    ops = {1: [], 2: [], 3: [], 4: []}  # +, -, * and /
    i: int = 0  # number of operators within ops

    value, pos = consume_value(seq, arr, pos)
    values.append(value)

    while pos < len(seq) and (not until or (seq[pos] != until)):
        operator, pos = consume_op(seq, pos)
        ops[operator].append(i)
        i += 1
        value, pos = consume_value(seq, arr, pos)
        values.append(value)

    # elementary operators can be applied on vectors the same way as on scalars
    while ops[3] or ops[4]:
        if (((ops[3] and ops[4]) and (ops[3][0] < ops[4][0]))
                or (ops[3] and not ops[4])):
            values[ops[3][0]+1] = values[ops[3][0]] * values[ops[3][0]+1]
            ops[3].pop(0)
        else:
            values[ops[4][0]+1] = values[ops[4][0]] / values[ops[4][0]+1]
            ops[4].pop(0)

    while ops[1] or ops[2]:
        if (((ops[1] and ops[2]) and (ops[1][0] < ops[2][0]))
                or (ops[1] and not ops[2])):
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


def consume_value(seq: str,
                  arr: dict[str, np.ndarray],
                  pos: int) -> Tuple[Value, int]:
    """Reads in a function or number values."""
    start = pos
    while pos < len(seq) and seq[pos] in string.ascii_lowercase:
        pos += 1
    if pos > start or seq[start] == "(":
        func_name = seq[start:pos]
        if func_name in arr:
            value = arr[func_name]
        else:
            pos = consume_parent(seq, pos)
            if func_name in FUNC_1:
                num, pos = consume_expr(seq, arr, pos, ")")
                pos = consume_parent(seq, pos)
                if func_name == "":
                    value = num
                else:
                    value = s_op(func_name, num)
            elif func_name in FUNC_2:
                num_1, pos = consume_expr(seq, arr, pos, ",")
                pos = consume_comma(seq, pos)
                num_2, pos = consume_expr(seq, arr, pos, ")")
                pos = consume_parent(seq, pos)
                if func_name == "pow":  # pow is good for arrays too
                    value = num_1 ** num_2
            else:
                raise ValueError(
                    f"{func_name} is not a function name in {seq}")
    else:
        value, pos = consume_number(seq, pos)

    return value, pos


def s_op(func_name: str, num: Value) -> Value:
    """Apply single argument operator func_name on num.

    Defined to reduce number of branches."""
    if isinstance(num, np.ndarray):
        if func_name == "sin":
            value = np.sin(num)
        elif func_name == "cos":
            value = np.cos(num)
        elif func_name == "sinh":
            value = np.sinh(num)
        elif func_name == "cosh":
            value = np.cosh(num)
    else:
        if func_name == "sin":
            value = math.sin(num)
        elif func_name == "cos":
            value = math.cos(num)
        elif func_name == "sinh":
            value = math.sinh(num)
        elif func_name == "cosh":
            value = math.cosh(num)
    return value


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
    test_data = {"x": np.array([10, 9, 8, 7, 6]),
                 "y": np.array([1.e-01, 2.e-01, 3.e-01, 4.e-01, 5.e-01]),
                 "z": np.array([1.e-06, 1.e-05, 1.e-04, 1.e-03, 1.e-02])}
    print("Apply a function on the data x, y and z:")
    while True:
        my_text = input()

        try:
            print(consume_expr(my_text, test_data, 0)[0])
        except ValueError as error:
            print(f"It is not a valid expression: {error}")
        except Exception as error:  # pylint: disable = broad-except
            print(f"It is not a valid expression: {error}")
