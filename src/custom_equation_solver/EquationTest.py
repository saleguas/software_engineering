from Function import Function
from Constant import Constant
from Variable import Variable
from SimplePower import Power
from Exponential import Exponential
from SimplePower import SimplePower
from Multiply import Multiply
from Add import Add
from Equation import Equation
import unittest


class EquationTest(unittest.TestCase):
    def test_solve_linear(self):
        left_function = Constant(10)
        right_function = Add([Multiply([Constant(2), SimplePower("x", Constant(1))]), Constant(4)])
        equation = Equation(left_function, right_function)
        solution, steps = equation.solve_linear()
        print(solution)
        for step in steps:
            print(step)
