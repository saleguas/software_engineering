from Function import Function
from Variable import Variable
from Constant import Constant
from Add import Add
from Multiply import Multiply
from SimplePower import SimplePower
from StaticFunctions import *


class Equation:
    def __init__(self, left_function: Function, right_function: Function):
        self.left_function = left_function
        self.right_function = right_function

    def is_linear(self):
        return self.left_function.is_linear() and self.right_function.is_linear()

    # Returns the solution or true or false is there are infinitely many or no solutions
    def solve_linear(self):
        steps = []
        # Simplify (distribute and combine like terms)
        """self.left_function.simplify()
        self.right_function.simplify()
        steps += "If applicable, simplify both sides of the equation using the distributive property. Then," \
                 "combine like terms: " + self.left_function.to_string() + " = " + self.right_function.to_string()"""

        self.left_function = distribute(self.left_function)
        self.right_function = distribute(self.right_function)
        steps += "If applicable, apply the distributive property, yielding " + self.left_function.to_string() + " = " +\
                 self.right_function.to_string()
        self.left_function.simplify()
        self.right_function.simplify()

        self.left_function = remove_nesting(self.left_function)
        self.right_function = remove_nesting(self.right_function)
        steps += "If applicable, simplify, yielding " + self.left_function.to_string() + " = " +\
                 self.right_function.to_string()

        # case 1: Both sides are constant
        if isinstance(self.left_function, Constant) and isinstance(self.right_function, Constant):
            if self.left_function == self.right_function:
                return True, ["This equation is always true"]
            else:
                return False, ["This equation is never true"]
        # case 2: Left side is constant: a = mx + b
        elif isinstance(self.left_function, Constant) and isinstance(self.right_function, Add) and \
                len(self.right_function.addends) == 2:
            constant = 0
            slope = 0
            variable = 0
            for addend in self.right_function.addends:
                if isinstance(addend, Constant):
                    constant = addend
                elif isinstance(addend, Multiply):
                    for factor in addend.factors:
                        if isinstance(factor, Constant):
                            slope = factor
                        elif isinstance(factor, SimplePower):
                            variable = factor
                        else:
                            return False, ["ERROR"]
                else:
                    return False, ["ERROR"]
            left_side_1 = self.left_function - constant
            left_side_2 = left_side_1/slope
            steps += ["Subtract " + constant.to_string() + " from both sides of the equation, yielding " +
                     self.left_function.to_string() + " - " + constant.to_string() + " = " +
                     self.right_function.to_string() + " - " + constant.to_string() + ".",
                     "Simplify: " + str(left_side_1) +  " = " + slope.to_string() + "*" + variable.to_string() + ".",
                     "Divide both sides by " + slope.to_string() + ": " + str(left_side_1) + "/" + slope.to_string() +
                     " = (" + slope.to_string() + variable.to_string() + ")/" + slope.to_string() + ".",
                     "Simplify: " + str(left_side_2) + " = " + variable.to_string()]
            return left_side_2, steps

        # case 3: Right side is constant
        elif isinstance(self.left_function, Add) and isinstance(self.right_function, Constant) and \
                len(self.left_function.addends) == 2:
            constant = 0
            slope = 0
            variable = 0
            for addend in self.left_function.addends:
                if isinstance(addend, Constant):
                    constant = addend
                elif isinstance(addend, Multiply):
                    for factor in addend.factors:
                        if isinstance(factor, Constant):
                            slope = factor
                        elif isinstance(factor, SimplePower):
                            variable = factor
                        else:
                            return False, ["ERROR"]
                else:
                    return False, ["ERROR"]
            right_side_1 = self.right_function - constant
            right_side_2 = right_side_1/slope
            steps = ["Subtract " + constant.to_string() + " from both sides of the equation, yielding " +
                     self.left_function.to_string() + " - " + constant.to_string() + " = " +
                     self.right_function.to_string() + " - " + constant.to_string() + ".",
                     "Simplify: " + slope.to_string() + "*" + variable.to_string() + " = " + str(right_side_1) + ".",
                     "Divide both sides by " + slope.to_string() + ": " +
                     "(" + slope.to_string() + variable.to_string() + ")/" + slope.to_string() + " = " +
                     str(right_side_1) + "/" + slope.to_string() + ".",
                     "Simplify: " + variable.to_string() + " = " + str(right_side_2)]
            return right_side_2, steps

        # case 4: Neither side is constant
        elif isinstance(self.left_function, Add) and isinstance(self.right_function, Add) and \
                len(self.left_function.addends) == 2 and len(self.right_function.addends) == 2:
            slope_left = 0
            variable_left = 0
            constant_left = 0
            slope_right = 0
            variable_right = 0
            constant_right = 0

            for addend in self.left_function.addends:
                if isinstance(addend, Multiply):
                    for factor in addend.factors:
                        if isinstance(factor, Constant):
                            slope_left = factor
                        elif isinstance(factor, SimplePower):
                            variable_left = factor.base
                        else:
                            return False, ["ERROR"]
                elif isinstance(addend, Constant):
                    constant_left = addend
                else:
                    return False, ["ERROR"]

            for addend in self.right_function.addends:
                if isinstance(addend, Multiply):
                    for factor in addend.factors:
                        if isinstance(factor, Constant):
                            slope_right = factor
                        elif isinstance(factor, SimplePower):
                            variable_right = factor.base
                        else:
                            return False, ["ERROR"]
                elif isinstance(addend, Constant):
                    constant_right = addend
                else:
                    return False, ["ERROR"]
            if variable_left != variable_right:
                return False, ["ERROR"]
            right_side_1 = self.right_function - constant
            right_side_2 = right_side_1/slope
            steps = ["Subtract " + constant.to_string() + " from both sides of the equation, yielding " +
                     self.left_function.to_string() + " - " + constant.to_string() + " = " +
                     self.right_function.to_string() + " - " + constant.to_string() + ".",
                     "Simplify: " + slope.to_string() + "*" + variable.to_string() + " = " + str(right_side_1) + ".",
                     "Divide both sides by " + slope.to_string() + ": " +
                     "(" + slope.to_string() + variable.to_string() + ")/" + slope.to_string() + " = " +
                     str(right_side_1) + "/" + slope.to_string() + ".",
                     "Simplify: " + variable.to_string() + " = " + str(right_side_2)]
            return right_side_2, steps

    def solve(self, var: Variable):
        # check for linearity
        if self.is_linear():
            return self.solve_linear()
        return None

    def to_string(self):
        return self.left_function.to_string() + " = " + self.right_function.to_string()
