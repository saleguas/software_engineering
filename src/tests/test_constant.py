import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tests"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "custom_equation_solver"))
from Constant import Constant
import pytest

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