from Function import Function
from Constant import Constant
from Variable import Variable
from SimplePower import Power
from Exponential import Exponential
from SimplePower import SimplePower
from Multiply import Multiply
from Add import Add
from Equation import Equation
from StaticFunctions import *
import pytest


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
    for step in steps:
        print(step)


def test_solve_linear_2():
    right_function = Constant(10)
    left_function = Add([Multiply([Constant(2), SimplePower("x", Constant(1))]), Constant(4)])
    equation = Equation(left_function, right_function)
    solution, steps = equation.solve_linear()
    assert solution == 3
    for step in steps:
        print(step)


def test_linear_equation_with_like_terms():
    left_function = Add([Multiply([Constant(3), SimplePower("x", Constant(1))]), Constant(0)])
    right_function = Add([Multiply([Constant(1), SimplePower("x", Constant(1))]), Constant(4)])
    equation = Equation(left_function, right_function)
    solution, steps = equation.solve_linear()
    for step in steps:
        print(step)
    assert solution == 2


def test_linear_equation_with_like_terms_2():
    left_function = Multiply([Constant(3), SimplePower("x", Constant(1))])
    right_function = Add([SimplePower("x", Constant(1)), Constant(4)])
    equation = Equation(left_function, right_function)
    solution, steps = equation.solve_linear()
    for step in steps:
        print(step)
    assert solution == 2


def test_linear_equation_with_distribution():
    left_function = Constant(15)
    right_function = Multiply([Add([SimplePower("x", Constant(1)), Constant(2)]), Constant(3)])
    equation = Equation(left_function, right_function)
    solution, steps = equation.solve_linear()
    for step in steps:
        print(step)
    assert solution == 3


def test_distribute():
    function = Multiply([Constant(5), Add([SimplePower("x", 1), Constant(2)])])
    function = distribute(function)
    assert function.to_string() == "5.0*x + 5.0*2.0"


def test_solve_linear_3():
    right_function = Constant(10)
    left_function = Multiply([Constant(2), Add([Multiply([Constant(2), SimplePower("x", Constant(1))]), Constant(4)])])
    equation = Equation(left_function, right_function)
    solution, steps = equation.solve_linear()
    assert solution == 0.5
    for step in steps:
        print(step)


def test_parse_string_1():
    test_input = "2*x +3 = 10"
    parsed_function = parse_string(test_input)
    solution, steps = parsed_function.solve_linear()
    assert solution == 3.5
    assert True


def test_parse_string_():
    test_input = "3*x*2 = 5"
    parsed_function = parse_string(test_input)
    # assert parsed_function.is_linear()
    solution, steps = parsed_function.solve_linear()
    assert solution == 5/6
    assert True


def test_parse_function_works_with_parentheses():
    passed = None
    solution = None
    try:
        test_input = "2*(x+3)+5=15"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed
    assert solution == 2


def test_standardize_linear_format():
    function = Add([SimplePower('x', Constant(1)), Constant(1)])  # x+1
    function = standardize_linear_format(function)  # should be 1x+1
    sample = Add([Multiply([Constant(1), SimplePower('x', 1)]), Constant(1)])
    assert isinstance(function, Add)
    for addend in function.addends:
        if isinstance(addend, Multiply):
            assert len(addend.factors) == 2
            assert (isinstance(addend.factors[0], Constant) and isinstance(addend.factors[0], SimplePower)) or \
                   (isinstance(addend.factors[1], Constant) and isinstance(addend.factors[0], SimplePower))
            if isinstance(addend.factors[0], Constant):
                assert addend.factors[0] == 1 and addend.factors[1].base == 'x' and addend.factors[1].power == 1
            else:
                assert addend.factors[1] == 1 and addend.factors[0].base == 'x' and addend.factors[0].power == 1
        elif isinstance(addend, Constant):
            assert addend == 1
        else:
            assert False


def test_solve_linear_1():
    left_function = Constant(10)
    right_function = Add([Multiply([Constant(2), SimplePower("x", Constant(1))]), Constant(4)])
    equation = Equation(left_function, right_function)
    solution, steps = equation.solve_linear()
    assert solution == 3.0
    for step in steps:
        print(step)


def test_linear_equation_with_like_terms_1():
    left_function = Add([Multiply([Constant(3), SimplePower("x", Constant(1))]), Constant(0)])
    right_function = Add([Multiply([Constant(1), SimplePower("x", Constant(1))]), Constant(4)])
    equation = Equation(left_function, right_function)
    solution, steps = equation.solve_linear()
    for step in steps:
        print(step)
    assert solution == 2


def test_parse_string_2():
    passed = None
    solution = None
    try:
        test_input = "5*x +4 = 14"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 2


def test_parse_string_many_spaces():
    passed = None
    solution = None
    try:
        test_input = "2 * x + 4 = 10"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


def test_parse_string_invalid_function_1():
    passed = None
    try:
        test_input = "2*+x+4=10"
        parsed_function = parse_string(test_input)
        passed = True
    except:
        passed = False
    assert passed == False


def test_parse_string_invalid_function_2():
    passed = None
    try:
        test_input = "2*x+4==10"
        parsed_function = parse_string(test_input)
        passed = True
    except:
        passed = False
    assert passed == False


def test_parse_string_several_consecutive_spaces():
    passed = None
    parsed_function = None
    try:
        test_input = "2*x+   4=10"
        parsed_function = parse_string(test_input)
        passed = True
    except:
        passed = False
    assert passed == True
    assert parsed_function.to_string() == "2.0*x + 4.0 = 10.0"


def test_parse_string_already_valid():
    passed = None
    solution = None
    try:
        test_input = "2*x+4=10"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


def test_parse_string_expression_only():
    passed = None
    try:
        test_input = "2*x+3"
        parsed_function = parse_string(test_input)
        passed = True
    except:
        passed = False
    assert passed == False


def test_parse_string_two_variables():
    passed = None
    try:
        test_input = "x+y=5"
        parsed_function = parse_string(test_input)
        passed = True
    except:
        passed = False
    assert passed == False


def test_parse_string_works_when_user_is_on_acid():
    passed = None
    solution = None
    try:
        test_input = "2*x#+4&=10_"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


def test_parse_function_coefficient_after_variable():
    passed = None
    solution = None
    try:
        test_input = "x*2+4=10"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


def test_parse_function_obligatory_empty_string_case():
    passed = None
    try:
        test_input = ""
        parsed_function = parse_string(test_input)
        passed = True
    except:
        passed = False
    assert passed == False


def test_parse_function_double_coefficients_1():
    passed = None
    solution = None
    try:
        test_input = "2*3*x+4=14"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 5 / 3


def test_parse_function_double_coefficients_2():
    passed = None
    solution = None
    try:
        test_input = "2*x*3+4=14"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 5 / 3


def test_parse_function_like_terms():
    passed = None
    solution = None
    try:
        test_input = "3*x+4=x+10"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


def test_parse_function_double_equals():
    passed = None
    try:
        test_input = "2*x+4=3*x+1=10"
        parsed_function = parse_string(test_input)
        passed = True
    except:
        passed = False
    assert passed == False


def test_parse_function_backwards_parentheses():
    passed = None
    try:
        test_input = "2*x)+4(=10"
        parsed_function = parse_string(test_input)
        passed = True
    except:
        passed = False
    assert passed == False


def test_parse_function_equals_sign_in_parentheses():
    passed = None
    try:
        test_input = "2*x+(4=10)"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == False


def test_parse_function_both_sides_in_parentheses():
    passed = None
    solution = None
    try:
        test_input = "(2*x+4)=(7+3)"
        parsed_function = parse_string(test_input)
        solution, steps = parsed_function.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


def test_is_linear_true():
    left_function = Add([Constant(4), Multiply([Constant(2), SimplePower("x", Constant(1))])])
    right_function = Constant(10)
    equation = Equation(left_function, right_function)
    assert equation.is_linear() == True


def test_is_linear_false():
    left_function = Constant(10)
    right_function = Add([Constant(4), Multiply([Constant(2), SimplePower("x", Constant(2))])])
    equation = Equation(left_function, right_function)
    assert equation.is_linear() == False


def test_is_linear_true_like_terms():
    left_function = Add([SimplePower("x", Constant(1)), Constant(10)])
    right_function = Add([Constant(4), Multiply([Constant(3), SimplePower("x", Constant(1))])])
    equation = Equation(left_function, right_function)
    assert equation.is_linear() == True


def test_is_linear_false_but_seems_true():
    left_function = Constant(16)
    right_function = Multiply([SimplePower("x", 1), SimplePower("x", Constant(1))])
    equation = Equation(left_function, right_function)
    assert equation.is_linear() == False


def test_to_string_1():
    left_function = Constant(10)
    right_function = Add([Constant(4), Multiply([Constant(2), SimplePower("x", Constant(1))])])
    equation = Equation(left_function, right_function)
    assert equation.to_string() == "10.0 = 4.0 + 2.0*x"


def test_to_string_2():
    left_function = Constant(17)
    right_function = Add([Multiply([Constant(5), SimplePower("x", Constant(1))]), Constant(7)])
    equation = Equation(left_function, right_function)
    assert equation.to_string() == "17.0 = 5.0*x + 7.0"


def test_solve_linear_multi_sum():
    passed = None
    solution = None
    try:
        left_function = Constant(10)
        right_function = Add(
            [Constant(5), Constant(5), Constant(-6), Multiply([Constant(2), SimplePower("x", Constant(1))])])
        equation = Equation(left_function, right_function)
        solution, steps = equation.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


def test_solve_linear_multi_product():
    passed = None
    solution = None
    try:
        left_function = Constant(10)
        right_function = Add(
            [Constant(4), Multiply([Constant(5), Constant(4), Constant(0.1), SimplePower("x", Constant(1))])])
        equation = Equation(left_function, right_function)
        solution, steps = equation.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


# def test_solve_linear_with_exponent_expression():
#     passed = None
#     solution = None
#     try:
#         left_function = Add([Constant(7), Multiply([Constant(5), SimplePower("x", Constant(1))])])
#         right_function = Add([Multiply([Constant(2), SimplePower("x", Add([Constant(3), Constant(-2)]))]), Constant(22)]) #here the exponent is a sum, but the sum's value is still 1
#         equation = Equation(left_function, right_function)
#         solution, steps = equation.solve_linear()
#         passed = True
#     except:
#         passed = False
#     assert passed == True
#     assert solution == 5

def test_solve_linear_negative_answer():
    passed = None
    solution = None
    try:
        left_function = Constant(3)
        right_function = Add([Constant(15), Multiply([Constant(3), SimplePower("x", Constant(1))])])
        equation = Equation(left_function, right_function)
        solution, steps = equation.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == -4


# def test_solve_linear_zero_power():
#     passed = None
#     solution = None
#     try:
#         left_function = Add([Constant(9), SimplePower("x", Constant(0))])
#         right_function = Add([Constant(4), Multiply([Constant(2), SimplePower("x", Constant(1))])])
#         equation = Equation(left_function, right_function)
#         solution, steps = equation.solve_linear()
#         passed = True
#     except:
#         passed = False
#     assert passed == True
#     assert solution == 3

def test_solve_linear_zero_power_times_variable():
    passed = None
    solution = None
    try:
        left_function = Add([Constant(4), Constant(6)])
        right_function = Add(
            [Constant(4), Multiply([Constant(2), SimplePower("x", Constant(1)), SimplePower("x", Constant(0))])])
        equation = Equation(left_function, right_function)
        solution, steps = equation.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


def test_solve_linear_nested_parentheses():
    passed = None
    solution = None
    try:
        left_function = Multiply(
            [Add([Constant(2), Multiply([Constant(2), SimplePower("x", Constant(1)), Constant(3)])]),
             Add([Constant(5.7), Constant(-3.7)])])
        right_function = Multiply([Constant(3), Add([Constant(10), Multiply([Constant(2), Constant(2), Constant(2)])])])
        equation = Equation(left_function, right_function)
        solution, steps = equation.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 25 / 6


def test_solve_linear_array_with_single_element():
    passed = None
    solution = None
    try:
        left_function = Add([Constant(10)])
        right_function = Add([Multiply([Constant(4)]), Multiply([Constant(2), SimplePower("x", Constant(1))])])
        equation = Equation(left_function, right_function)
        solution, steps = equation.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3


def test_standardize_linear_format_1():
    function = Add([SimplePower('x', Constant(1)), Constant(1)])
    function = standardize_linear_format(function)
    assert isinstance(function, Add)
    for addend in function.addends:
        if isinstance(addend, Multiply):
            assert len(addend.factors) == 2
            assert (isinstance(addend.factors[0], Constant) and isinstance(addend.factors[0], SimplePower)) or \
                   (isinstance(addend.factors[1], Constant) and isinstance(addend.factors[0], SimplePower))
            if isinstance(addend.factors[0], Constant):
                assert addend.factors[0] == 1 and addend.factors[1].base == 'x' and addend.factors[1].power == 1
            else:
                assert addend.factors[1] == 1 and addend.factors[0].base == 'x' and addend.factors[0].power == 1
        elif isinstance(addend, Constant):
            assert addend == 1
        else:
            assert False


def test_standardize_linear_format_2():
    function = Add([Constant(0)])
    function = standardize_linear_format(function)
    assert isinstance(function, Add)
    for addend in function.addends:
        if isinstance(addend, Multiply):
            assert len(addend.factors) == 2
            assert (isinstance(addend.factors[0], Constant) and isinstance(addend.factors[0], SimplePower)) or \
                   (isinstance(addend.factors[1], Constant) and isinstance(addend.factors[0], SimplePower))
            if isinstance(addend.factors[0], Constant):
                assert addend.factors[0] == 1 and addend.factors[1].base == 'x' and addend.factors[1].power == 1
            else:
                assert addend.factors[1] == 1 and addend.factors[0].base == 'x' and addend.factors[0].power == 1
        elif isinstance(addend, Constant):
            assert addend == 0
        else:
            assert False


def test_standardize_linear_format_3():
    function = Add([SimplePower('x', Constant(1))])
    function = standardize_linear_format(function)
    assert isinstance(function, Add)
    for addend in function.addends:
        if isinstance(addend, Multiply):
            assert len(addend.factors) == 2
            assert (isinstance(addend.factors[0], Constant) and isinstance(addend.factors[0], SimplePower)) or \
                   (isinstance(addend.factors[1], Constant) and isinstance(addend.factors[0], SimplePower))
            if isinstance(addend.factors[0], Constant):
                assert addend.factors[0] == 1 and addend.factors[1].base == 'x' and addend.factors[1].power == 1
            else:
                assert addend.factors[1] == 1 and addend.factors[0].base == 'x' and addend.factors[0].power == 1
        elif isinstance(addend, Constant):
            assert addend == 1
        else:
            assert False


def test_standardize_linear_format_4():
    function = Add([SimplePower('x', Constant(1)), Constant(4)])
    function = standardize_linear_format(function)
    assert isinstance(function, Add)
    for addend in function.addends:
        if isinstance(addend, Multiply):
            assert len(addend.factors) == 2
            assert (isinstance(addend.factors[0], Constant) and isinstance(addend.factors[0], SimplePower)) or \
                   (isinstance(addend.factors[1], Constant) and isinstance(addend.factors[0], SimplePower))
            if isinstance(addend.factors[0], Constant):
                assert addend.factors[0] == 1 and addend.factors[1].base == 'x' and addend.factors[1].power == 1
            else:
                assert addend.factors[1] == 1 and addend.factors[0].base == 'x' and addend.factors[0].power == 1
        elif isinstance(addend, Constant):
            assert addend == 4
        else:
            assert False


def test_standardize_linear_format_5():
    function = Add([Multiply([SimplePower('x', Constant(1)), Constant(2)]), Constant(3)])
    function = standardize_linear_format(function)
    assert isinstance(function, Add)
    for addend in function.addends:
        if isinstance(addend, Multiply):
            assert len(addend.factors) == 2
            assert (isinstance(addend.factors[0], Constant) and isinstance(addend.factors[0], SimplePower)) or \
                   (isinstance(addend.factors[1], Constant) and isinstance(addend.factors[0], SimplePower))
            if isinstance(addend.factors[0], Constant):
                assert addend.factors[0] == 2 and addend.factors[1].base == 'x' and addend.factors[1].power == 1
            else:
                assert addend.factors[1] == 2 and addend.factors[0].base == 'x' and addend.factors[0].power == 1
        elif isinstance(addend, Constant):
            assert addend == 3
        else:
            assert False


@pytest.mark.parametrize(
    ('input2', 'expected2'),
    (
            pytest.param('dawda', False, id='test string'),
            pytest.param(4.5, True, id='test float'),
            pytest.param(3, True, id='test int'),
            pytest.param('+', False, id='test char'),
    )
)
def test_is_float(input2, expected2):
    assert is_float(input2) == expected2


def test_constant_evaluate():
    c = Constant(3.3)
    assert c.evaluate(3) == 3.3


def test_constant_is_linear():
    c = Constant(5.6)
    assert c.is_linear() == True


def test_constant_is_quadratic():
    c = Constant(2.0)
    assert c.is_quadratic() == True


def test_constant_to_string():
    c = Constant(1.6)
    assert c.to_string() == "1.6"


def test_constant_simplify():
    c = Constant(1.2)
    assert c.simplify() == 1.2


@pytest.mark.parametrize(
    ('input1', 'input1_1', 'expected1'),
    (
            pytest.param(SimplePower('x', 2), SimplePower('x', 3), 5, id='x^2*x^3'),
            pytest.param(SimplePower('x', 1), SimplePower('x', 1), 2, id='x*x'),
            pytest.param(SimplePower('x', 3), SimplePower('x', 4), 7, id='x^3*x^4'),
            pytest.param(SimplePower('x', 20), SimplePower('x', 20), 40, id='x^20*x^20'),
            pytest.param(SimplePower('x', 9), SimplePower('x', 3), 12, id='x^9*x^3'),
    )
)
def test_multiply_combine_powers_2(input1, input1_1, expected1):
    function = Multiply([input1, input1_1])
    function.combine_powers()
    assert isinstance(function, Multiply)
    assert len(function.factors) == 1
    assert isinstance(function.factors[0], SimplePower)
    assert function.factors[0].base == 'x'
    assert function.factors[0].power == expected1


@pytest.mark.parametrize(
    ('input2', 'expected2'),
    (
            pytest.param(Multiply([Constant(5)]), True, id='test 5'),
            pytest.param(Multiply([SimplePower('x', 1), Constant(3)]), True, id='test 3x'),
            pytest.param(Multiply([SimplePower('x', 1)]), True, id='test x'),
            pytest.param(Multiply([SimplePower('x', 2)]), False, id='test x^2'),
            pytest.param(Multiply([Constant(3), SimplePower('x', 2)]), False, id='test 3x^2'),
    )
)
def test_is_linear(input2, expected2):
    assert input2.is_linear() == expected2


def test_simple_power_evaluate():
    sp = SimplePower("x", 3)
    assert sp.evaluate(2) == 8


def test_simple_power_is_linear():
    sp = SimplePower("x", 5)
    assert sp.is_linear() == False


def test_simple_power_to_string():
    sp = SimplePower("x", 1)
    assert sp.to_string() == "x"


def test_variable_evaluate():
    c = Variable("y")
    assert c.evaluate(3) == 3


def test_variable_is_linear():
    c = Variable("z")
    assert c.is_linear() == True


def test_variable_to_string():
    c = Variable("v")
    assert c.to_string() == "v"


def test_solve_quadratic_1():
    left_function = Add([Multiply([SimplePower("x", Constant(2)), Constant(2)]),
                         Multiply([SimplePower("x", Constant(1)), Constant(-1)]), Constant(5)])
    right_function = Add([Multiply([SimplePower("x", Constant(2)), Constant(-5)]),
                          Multiply([SimplePower("x", Constant(1)), Constant(0.5)]), Constant(10)])
    equation = Equation(left_function, right_function)
    assert equation.is_quadratic()
    solution, steps = equation.solve_quadratic()
    assert -.745 < solution[1] < -.744
    assert .959 < solution[0] < .96


def test_solve_quadratic_2():
    left_function = SimplePower('x', Constant(2))
    right_function = Constant(1)
    equation = Equation(left_function, right_function)
    assert equation.is_quadratic()
    solution, steps = equation.solve_quadratic()
    assert solution[0] == 1
    assert solution[1] == -1


def test_solve_quadratic_3():
    left_function = Add([Multiply([SimplePower("x", Constant(2)), Constant(2)]),
                         Multiply([SimplePower("x", Constant(1)), Constant(-1)]), Constant(5)])
    right_function = Multiply([SimplePower("x", Constant(2)), Constant(2)])
    equation = Equation(left_function, right_function)
    assert equation.is_quadratic()
    solution, steps = equation.solve_quadratic()
    assert solution == 5


def test_solve_quadratic_4():
    left_function = Add([Multiply([SimplePower("x", Constant(2)), Constant(.5)]),
                         Multiply([SimplePower("x", Constant(1)), Constant(-1)]), Constant(5),
                         Multiply([SimplePower("x", Constant(2)), Constant(.5)]), Constant(2)])
    right_function = Add([Multiply([SimplePower("x", Constant(1)), Constant(0.5)]), Constant(10)])
    equation = Equation(left_function, right_function)
    assert equation.is_quadratic()
    solution, steps = equation.solve_quadratic()
    assert -1.138 < solution[1] < -1.137
    assert 2.637 < solution[0] < 2.638


def test_solve_quadratic_5():
    left_function = Add([Multiply([SimplePower("x", Constant(2)), Constant(.5)]),
                         Multiply([SimplePower("x", Constant(1)), Constant(-1)]), Constant(5),
                         Multiply([SimplePower("x", Constant(2)), Constant(.5)]), Constant(2)])
    right_function = Add([Multiply([SimplePower("x", Constant(2)), Constant(.5)]),
                          Multiply([SimplePower("x", Constant(1)), Constant(-1)]), Constant(5),
                          Multiply([SimplePower("x", Constant(2)), Constant(.5)]), Constant(2)])
    equation = Equation(left_function, right_function)
    assert equation.is_quadratic()
    solution, steps = equation.solve_quadratic()
    assert solution


def test_distribute_2():
    function = Multiply([Constant(10), Add([Constant(5), SimplePower('x', Constant(2))])])
    function = distribute(function)
    assert function.to_string() == "10.0*5.0 + 10.0*x^2.0"


def test_distribute_3():
    function = Multiply([Constant(10), Add([SimplePower('x', Constant(2)), Constant(5)])])
    function = distribute(function)
    assert function.to_string() == "10.0*x^2.0 + 10.0*5.0"


def test_distribute_4():
    function = Multiply([Add([SimplePower('x', Constant(3)), Multiply([SimplePower('x', Constant(4)), Constant(5)])]),
                         Add([SimplePower('x', Constant(2)), Constant(5)])])
    function = distribute(function)
    assert function.to_string() == "x^3.0*x^2.0 + x^3.0*5.0 + x^4.0*5.0*x^2.0 + x^4.0*5.0*5.0"


def test_multiply_to_string_1():
    function = Multiply([Constant(10), Add([Constant(5), SimplePower('x', Constant(2))])])
    assert function.to_string() == "10.0*(5.0 + x^2.0)"


def test_multiply_to_string_2():
    function = Multiply([Constant(10), Constant(5)])
    assert function.to_string() == "10.0*5.0"


def test_multiply_to_string_3():
    function = Multiply([Constant(1.5), SimplePower("x", Constant(2)), Constant(.5)])
    assert function.to_string() == "1.5*x^2.0*0.5"


def test_multiply_to_string_4():
    function = Multiply([Add([Multiply([SimplePower("x", Constant(2)), Constant(.5)]),
                              Multiply([SimplePower("x", Constant(1)), Constant(-1)]), Constant(5),
                              Multiply([SimplePower("x", Constant(2)), Constant(.5)]), Constant(2)]),
                         Add([Multiply([SimplePower("x", Constant(2)), Constant(.5)]),
                              Multiply([SimplePower("x", Constant(1)), Constant(-1)]), Constant(5),
                              Multiply([SimplePower("x", Constant(2)), Constant(.5)]), Constant(2)])])
    assert function.to_string() == '(x^2.0*0.5 + x*-1.0 + 5.0 + x^2.0*0.5 + 2.0)*(x^2.0*0.5 + x*-1.0 + 5.0 + x^2.0*0.5 + 2.0)'


def test_remove_nesting_add():
    function1 = remove_nesting(Add([Constant(4), Add([Constant(3), Constant(3)])]))
    function2 = Add([Constant(4), Constant(3), Constant(3)])
    assert function1.to_string() == function2.to_string()


def test_remove_nesting_multiply():
    function1 = remove_nesting(Multiply([Constant(3), Multiply([Constant(2), Constant(2)])]))
    function2 = Multiply([Constant(3), Constant(2), Constant(2)])
    assert function1.to_string() == function2.to_string()


def test_remove_nesting_with_variable():
    function1 = remove_nesting(Multiply([Constant(3), Multiply([SimplePower("x", Constant(1)), Constant(2)])]))
    function2 = Multiply([Constant(3), SimplePower("x", Constant(1)), Constant(2)])
    assert function1.to_string() == function2.to_string()


def test_balanced_delimiters_valid():
    function = "2*(x+5)"
    assert balanced_delimiters(function) == True


def test_balanced_delimeters_invalid():
    function = "2*(x+5)+3)"
    assert balanced_delimiters(function) == False


def test_balanced_delimiters_backwards():
    function = "2)*x+(5"
    assert balanced_delimiters(function) == False


def test_balanced_delimiters_foil_method():
    # I am using parse_string, but the part that is tricky involves testing the balanced delimiters
    input = "(x+2)*(x+5)=40"
    assert balanced_delimiters(input)


def test_evaluate_multiply_1():
    function = Multiply([SimplePower('x', 1), Constant(3)])
    assert function.evaluate(10.5) == 31.5


def test_evaluate_multiply_2():
    function = Multiply([Constant(3), SimplePower("x", Constant(1)), Constant(2)])
    assert function.evaluate(-3) == -18


def test_evaluate_multiply_3():
    function = Multiply([Constant(3), Constant(2), Constant(2)])
    assert function.evaluate(-10.3242) == 12


def test_evaluate_multiply_4():
    function = Multiply([SimplePower("x", Constant(2)), Constant(.5)])
    assert function.evaluate(3) == 4.5


def test_remove_nested_multiply_1():
    function = Multiply([SimplePower("x", Constant(2)), Constant(.5),
                         Multiply([SimplePower("x", Constant(2)), Constant(.5),
                                   Multiply([SimplePower("x", Constant(2)), Constant(.5)])])])
    function.remove_nested_multiply()
    assert function.to_string() == 'x^2.0*0.5*x^2.0*0.5*x^2.0*0.5'


def test_remove_nested_multiply_2():
    function = Multiply([SimplePower("x", Constant(2)), Constant(.5),
                         Multiply([SimplePower("x", Constant(2)), Constant(.5),
                                   Multiply([Constant(1)])])])
    function.remove_nested_multiply()
    assert function.to_string() == 'x^2.0*0.5*x^2.0*0.5*1.0'


def test_multiply_combine_constants_1():
    function = Multiply([SimplePower("x", Constant(2)), Constant(.5),
                         Multiply([SimplePower("x", Constant(2)), Constant(.5),
                                   Multiply([Constant(1)])])])
    function.remove_nested_multiply()
    function.combine_constants()
    assert function.to_string() == '0.25*x^2.0*x^2.0'


def test_multiply_combine_constants_2():
    function = Multiply([SimplePower("x", Constant(2)), Constant(.5),
                         Multiply([SimplePower("x", Constant(2)), Constant(.5),
                                   Multiply([SimplePower("x", Constant(2)), Constant(.5)])])])
    function.remove_nested_multiply()
    function.combine_constants()
    assert function.to_string() == '0.125*x^2.0*x^2.0*x^2.0'


def test_multiply_combine_constants_3():
    function = Multiply([Constant(5), Add([Constant(8), SimplePower('x', Constant(3))]), Constant(10)])
    function.remove_nested_multiply()
    function.combine_constants()
    assert function.to_string() == '50.0*(8.0 + x^3.0)'

def test_parse_string_additional_1():
    input_string = "2*(x+x+x-3.1*x) = 8*(5*x)-3*x+5"
    equ = parse_string(input_string)
    solution, steps = equ.solve_linear()
    assert -.1345 < solution < -.1344


def test_parse_string_additional_2():
    input_string = "2*(x+x+x+3.1*x) = 8*(5*x)+3*x+5"
    equ = parse_string(input_string)
    solution, steps = equ.solve_linear()
    assert -.1624 < solution < -.1623


def test_parse_string_additional_3():
    input_string = "-2*x^2-3*x-8 = -17-85*x-10*x^2"
    equ = parse_string(input_string)
    solution, steps = equ.solve_quadratic()
    assert -10.14 < solution[1] < -10.139
    assert -.111 < solution[0] < -.1109
