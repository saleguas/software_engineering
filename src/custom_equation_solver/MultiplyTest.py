from Function import Function
from Constant import Constant
from Variable import Variable
from SimplePower import Power
from Exponential import Exponential
from SimplePower import SimplePower
from Multiply import Multiply
import pytest


def test_combine_constants():
    product = Multiply([1, 3, 1, Constant(2), Constant(-1.5), 0.1])
    product.combine_constants()
    # test that product is length 1
    assert len(product.factors) == 1
    # test that product is correct
    assert product.factors[0] == Constant(-0.9)


def test_remove_nested_multiply():
    product = Multiply([8, Multiply([Multiply([3, Constant(0.5)]), Constant(-2)])])
    product.remove_nested_multiply()
    # test that product is length 4
    assert len(product.factors) == 4
    # test that product is correct
    assert product.factors == [8, 3, 0.5, -2]


def test_combine_powers():
    product = Multiply([5, SimplePower("x", 2), SimplePower("x", 3), SimplePower("x", 0.5),
                        SimplePower("y", -2), SimplePower("x", 3), SimplePower("y", 10)])
    product.combine_powers()
    # test the length is correct
    assert len(product.factors) == 3
    # test that product is correct
    assert product.factors[0] == 5
    if product.factors[1].base == "x":
        assert product.factors[1].power == 8.5
        assert product.factors[2].base == "y"
        assert product.factors[2].power == 8
    elif product.factors[1].base == "y":
        assert product.factors[1].power == 8
        assert product.factors[2].base == "x"
        assert product.factors[2].power == 8.5
    else:
        assert False


def test_simplify():
    product = Multiply([8, Multiply([Multiply([3, Constant(0.5)]), Constant(-2)])])
    product.simplify()
    # test that product is length 1
    assert len(product.factors) == 1
    # test that product is correct
    assert product.factors == [-24]
