"""Test the single_arg."""

from math import sin  # pylint: disable=unused-import
import copy
import numpy as np
import multi_arg as ma


np.random.seed(0)
ma_data = {"x": np.random.random(8)*6}

# pylint: disable=eval-used


def test_constant_nested_function():
    """Nested expressions."""
    examples = ["3",
                "1+2*(3+4)",
                "(1)+7*((22))",
                "sin(pow(0.1,2))+3"]

    for example in examples:
        assert (ma.consume_expr(example, ma_data)[0] - eval(example)) == 0


def test_elementary():
    """Simplest binary operations."""
    examples = ["1",
                "x+1",
                "x-1",
                "x*2",
                "x/2",
                "1+x",
                "1-x",
                "2*x",
                "2/x"]
    x = ma_data["x"]  # pylint: disable=unused-variable
    for example in examples:
        assert np.sum((ma.consume_expr(example, ma_data)
                      [0] - eval(example))) == 0


def test_single_occurrance_nested():
    """Single occurrance of x in nested function."""
    examples = ["pow(sin(x),2)+pow(cos(0.1),2)",
                "1+(sin(sin(x/100)/100)*1e4)"]

    x = ma_data["x"]  # pylint: disable=unused-variable
    for example in examples:
        for_eval = example
        for func_1 in ma.FUNC_S:
            for_eval = for_eval.replace(func_1, "np." + func_1)
        assert np.sum((ma.consume_expr(example, ma_data)
                      [0] - eval(for_eval))) == 0


def test_multioccur():
    """Multiple occurrance of x"""
    examples = ["pow(sin(x),2)+pow(cos(x),2)-1",
                "sin(2*x)-2*sin(x)*cos(x)"]

    x = ma_data["x"]  # pylint: disable=unused-variable
    for example in examples:
        res = ma.consume_expr(example, ma_data)
        np.testing.assert_almost_equal(res[0], 0)

# pylint: enable=eval-used
