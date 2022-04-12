import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tests"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "custom_equation_solver"))
from Variable import Variable
import pytest

def test_variable_evaluate():
    c = Variable("y")
    assert c.evaluate(3) == 3

def test_variable_is_linear():
    c = Variable("z")
    assert c.is_linear() == True

def test_variable_to_string():
    c = Variable("v")
    assert c.to_string() == "v"