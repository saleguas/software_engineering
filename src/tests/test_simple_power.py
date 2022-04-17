import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tests"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "custom_equation_solver"))
from SimplePower import SimplePower
import pytest

def test_simple_power_evaluate():
    sp = SimplePower("x",3)
    assert sp.evaluate(2) == 8

def test_simple_power_is_linear():
    sp = SimplePower("x",5)
    assert sp.is_linear() == False

def test_simple_power_to_string():
    sp = SimplePower("x",1)
    assert sp.to_string() == "x"


