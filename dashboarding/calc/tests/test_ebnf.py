"""Test the ebnf_full expression evaluator."""


from math import sin  # pylint: disable=unused-import
from ebnf_full import consume_number, consume_expr

# pylint: disable=eval-used


def test_consume_number() -> None:
    """Test reading in numbers,
    neglect the precision lost with exponential notation."""
    examples = ["1",
                "1e3",
                "0.5",
                "-12.32",
                "-1.32e-7",
                "6e023"]
    for example in examples:
        assert (consume_number(example)[0] - eval(example)) == 0


def test_consume_elementary() -> None:
    """Numbers and elementary operators."""
    examples = ["1+2",
                "1+2*3",
                "1+2/4*4-11+21/32-5*2*41+3+3"]
    for example in examples:
        assert (consume_expr(example)[0] - eval(example)) == 0


def test_consume_function() -> None:
    """1 or 2 argument functions."""
    examples = ["sin(1/100)",
                "(1)",
                "pow(3.14159,1+1)"]
    for example in examples:
        assert (consume_expr(example)[0] - eval(example)) == 0


def test_consume_nested_function() -> None:
    """Nested expressions."""
    examples = ["1+2*(3+4)",
                "(1)+7*((22))",
                "sin(pow(0.1,2))+3"]
    for example in examples:
        assert (consume_expr(example)[0] - eval(example)) == 0
