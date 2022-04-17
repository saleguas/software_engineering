import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tests"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "custom_equation_solver"))

from Multiply import Multiply
from Constant import Constant
from SimplePower import SimplePower
from Add import Add
import pytest


@pytest.mark.parametrize(
    ('input1','input1_1','expected1'),
    (
        pytest.param(SimplePower('x',2),SimplePower('x',3),5,id='x^2*x^3'),
        pytest.param(SimplePower('x',1),SimplePower('x',1),2,id='x*x'),
        pytest.param(SimplePower('x',3),SimplePower('x',4),7,id='x^3*x^4'),
        pytest.param(SimplePower('x',20),SimplePower('x',20),40,id='x^20*x^20'),
        pytest.param(SimplePower('x',9),SimplePower('x',3),12,id='x^9*x^3'),

    )
)
def test_multiply_combine_powers(input1,input1_1,expected1):
    function = Multiply([input1,input1_1])
    function.combine_powers()
    assert isinstance(function,Multiply)
    assert len(function.factors) == 1
    assert isinstance(function.factors[0],SimplePower)
    assert function.factors[0].base == 'x'
    assert function.factors[0].power == expected1

@pytest.mark.parametrize(
    ('input2','expected2'),
    (
        pytest.param(Multiply([Constant(5)]),True,id='test 5'),
        pytest.param(Multiply([SimplePower('x',1),Constant(3)]),True,id='test 3x'),
        pytest.param(Multiply([SimplePower('x',1)]),True,id='test x'),
        pytest.param(Multiply([SimplePower('x',2)]),False,id='test x^2'),
        pytest.param(Multiply([Constant(3),SimplePower('x',2)]),False,id='test 3x^2'),
    )
)
def test_is_linear(input2,expected2):
    assert input2.is_linear() == expected2
