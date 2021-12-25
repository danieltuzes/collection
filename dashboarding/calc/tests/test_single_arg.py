"""Test the single_arg."""

from math import sin  # pylint: disable=unused-import
import re
import numpy as np
import single_arg as sa


np.random.seed(0)
data = np.random.random(8)*6

# pylint: disable=eval-used


def test_constant_nested_function():
    """Nested expressions."""
    examples = ["1+2*(3+4)",
                "(1)+7*((22))",
                "sin(pow(0.1,2))+3"]
    for example in examples:
        assert (sa.consume_expr(example, data, "x")[0] - eval(example)) == 0


def test_elementary():
    """Simplest binary operations."""
    examples = ["data+1",
                "data-1",
                "data*2",
                "data/2",
                "1+data",
                "1-data",
                "2*data",
                "2/data"]
    for example in examples:
        assert np.sum((sa.consume_expr(example, data, "data")
                      [0] - eval(example))) == 0


def test_single_occurrance_nested():
    """Single occurrance of x in nested function."""
    examples = ["pow(sin(data),2)+pow(cos(0.1),2)",
                "1+(sin(sin(data/100)/100)*1e4)"]
    for example in examples:
        for_eval = example
        for func_1 in sa.FUNC_S:
            for_eval = for_eval.replace(func_1, "np." + func_1)
        assert np.sum((sa.consume_expr(example, data, "data")
                      [0] - eval(for_eval))) == 0


def test_multioccur():
    """Multiple occurrance of x"""
    examples = ["pow(sin(data),2)+pow(cos(data),2)-1",
                "sin(2*data)-2*sin(data)*cos(data)"]
    for example in examples:
        res = sa.consume_expr(example, data, "data")
        np.testing.assert_almost_equal(res[0], 0)

# pylint: enable=eval-used
