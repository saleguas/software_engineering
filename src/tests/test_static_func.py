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

@pytest.mark.parametrize(
    ('input1','expected1'),
    (
        pytest.param(Constant(1),None,id='test x+1'),
        pytest.param(2,None,id='test x+2'),
        pytest.param(20,None,id='test x+20'),
    )
)
def test_standardize_linear_format(input1,expected1):
    pass


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

