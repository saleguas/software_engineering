from Function import Function
from Constant import Constant
from Variable import Variable
from SimplePower import Power
from Exponential import Exponential
from SimplePower import SimplePower
from Multiply import Multiply
from Add import Add
import pytest
# import unittest


def test_combine_like_terms():
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
