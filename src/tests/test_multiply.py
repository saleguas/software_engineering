import sys, os

from custom_equation_solver.Constant import Constant

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tests"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "custom_equation_solver"))

from Multiply import Multiply
import pytest

@pytest.mark.parametrize(
    ('input1','expected1'),
    (
        pytest.param(Multiply([Constant(5),Constant(2)]),None,id='test x+1'),
    )
)
def test_multiply_combine_powers(input1,expected1):
    pass

@pytest.mark.parametrize(
    ('input2','expected2'),
    (
        pytest.param(Multiply([Constant(5),Constant(2)]),None,id='test x+1'),
    )
)
def test_simplify(input2,expected2):
    pass

@pytest.mark.parametrize(
    ('input3','expected3'),
    (
        pytest.param(Multiply([Constant(5),Constant(2)]),None,id='test x+1'),
    )
)
def test_is_linear(input3,expected3):
    pass

@pytest.mark.parametrize(
    ('input4','expected4'),
    (
        pytest.param(Multiply([Constant(5),Constant(2)]),None,id='test x+1'),
    )
)
def test_to_string(input4,expected4):
    pass
