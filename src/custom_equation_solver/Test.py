from Function import Function
from Constant import Constant
from Variable import Variable
from SimplePower import Power
from Exponential import Exponential
from SimplePower import SimplePower
from Multiply import Multiply
from Add import Add
from Equation import Equation
import pytest
from StaticFunctions import *


def test_multiply_combine_constants():
    product = Multiply([1, 3, 1, Constant(2), Constant(-1.5), 0.1])
    product.combine_constants()
    # test that product is length 1
    assert len(product.factors) == 1
    # test that product is correct
    assert product.factors[0] == Constant(-0.9)


def test_multiply_remove_nested_multiply():
    product = Multiply([8, Multiply([Multiply([3, Constant(0.5)]), Constant(-2)])])
    product.remove_nested_multiply()
    # test that product is length 4
    assert len(product.factors) == 4
    # test that product is correct
    assert product.factors == [8, 3, 0.5, -2]


def test_multiply_combine_powers():
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


def test_multiply_simplify():
    product = Multiply([8, Multiply([Multiply([3, Constant(0.5)]), Constant(-2)])])
    product.simplify()
    # test that product is length 1
    assert len(product.factors) == 1
    # test that product is correct
    assert product.factors == [-24]


def test_add_combine_like_terms():
    addends = Add([3, SimplePower("x", 3.5), -8, Multiply([SimplePower("x", -.7), 5]),
                   SimplePower("x", -.7), Multiply([-.4, SimplePower("x", 3.5)])])
    addends.combine_like_terms()
    assert len(addends.addends) == 3
    for term in addends.addends:
        if isinstance(term, int) or isinstance(term, float):
            assert term == -5
        elif isinstance(term, Multiply):
            assert len(term.factors) == 2
            if isinstance(term.factors[0], Constant):
                assert term.factors[0] == 6.0 or term.factors[0] == .6
                assert term.factors[1].base == "x"
                assert term.factors[1].power == 3.5 or term.factors[1].power == -.7
            else:
                assert term.factors[1] == 6.0 or term.factors[1] == .6
                assert term.factors[0].base == "x"
                assert term.factors[0].power == 3.5 or term.factors[0].power == -.7
        else:
            assert 0 == 1


def test_solve_linear():
    left_function = Constant(10)
    right_function = Add([Multiply([Constant(2), SimplePower("x", Constant(1))]), Constant(4)])
    equation = Equation(left_function, right_function)
    solution, steps = equation.solve_linear()
    assert solution == 3.0
    print(solution)
    for step in steps:
        print(step)


def test_solve_linear_2():
    right_function = Constant(10)
    left_function = Add([Multiply([Constant(2), SimplePower("x", Constant(1))]), Constant(4)])
    equation = Equation(left_function, right_function)
    solution, steps = equation.solve_linear()
    print(solution)
    for step in steps:
        print(step)


# need to automate
def test_distribute():
    function = Multiply([5, Add([SimplePower("x", 1), 2])])
    function = distribute(function)
    print("hi")
    # print(function.to_string())

# need to automate
# def test_solve_linear_3():
#    right_function = Constant(10)
#    left_function = Multiply([Constant(2), Add([Multiply([Constant(2), SimplePower("x", Constant(1))]), Constant(4)])])
#    equation = Equation(left_function, right_function)
#    solution, steps = equation.solve_linear()
#    print(solution)
#    for step in steps:
#        print(step)