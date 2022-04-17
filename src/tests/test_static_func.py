import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tests"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "custom_equation_solver"))

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


def test_distribute():
    pass

def test_remove_nesting():
    pass
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
    function = Add([SimplePower('x',Constant(1))])
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
    function = Add([SimplePower('x',Constant(1)),Constant(4)])
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
    function = Add([Multiply([SimplePower('x',Constant(1)),2]),Constant(3)])
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
            assert addend == 3
        else:
            assert False

@pytest.mark.parametrize(
    ('input2','expected2'),
    (
        pytest.param('dawda',False,id='test string'),
        pytest.param(4.5,True,id='test float'),
        pytest.param(3,True,id='test int'),
        pytest.param('+',False,id='test char'),

    )
)
def test_is_float(input2,expected2):
    assert is_float(input2) == expected2

def balanced_delim():
    pass

def test_remove_nesting_add():
    function1 = remove_nesting(Add([Constant(4), Add([Constant(3), Constant(3)])]))
    function2 = Add([Constant(4), Constant(3), Constant(3)])
    assert function1 == function2

def test_remove_nesting_multiply():
    function1 = remove_nesting(Multiply([Constant(3), Multiply([Constant(2), Constant(2)])]))
    function2 = Multiply([Constant(3), Constant(2), Constant(2)])
    assert function1 == function2

def test_remove_nesting_with_variable():
    function1 = remove_nesting(Multiply([Constant(3), Multiply([SimplePower("x", Constant(1)), Constant(2)])]))
    function2 = Multiply([Constant(3), SimplePower("x", Constant(1)), Constant(2)])
    assert function1 == function2

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
    #I am using parse_string, but the part that is tricky involves testing the balanced delimiters
    passed = None
    solution = None
    try:
        input = "(x+2)*(x+5)=40"
        parsed_input = parse_string(input)
        solution, steps = parsed_input.solve_linear()
        passed = True
    except:
        passed = False
    assert passed == True
    assert solution == 3
