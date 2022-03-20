from Function import Function
from Variable import Variable
from Constant import Constant
from Add import Add
from Multiply import Multiply
from SimplePower import SimplePower


class Equation:
    def __init__(self, left_function: Function, right_function: Function):
        self.left_function = left_function
        self.right_function = right_function

    def is_linear(self):
        return self.left_function.is_linear() and self.right_function.is_linear()

    # Returns the solution or true or false is there are infinitely many or no solutions
    def solve_linear(self):
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
            steps = ["Subtract " + constant.to_string() + " from both sides of the equation, yielding " +
                     self.left_function.to_string() + " - " + constant.to_string() + " = " +
                     self.right_function.to_string() + " - " + constant.to_string() + ".",
                     "Simplify: " + str(left_side_1) +  " = " + slope.to_string() + "*" + variable.to_string() + ".",
                     "Divide both sides by " + slope.to_string() + ": " + str(left_side_1) + "/" + slope.to_string() +
                     " = (" + slope.to_string() + variable.to_string() + ")/" + slope.to_string() + ".",
                     "Simplify: " + str(left_side_2) + " = " + variable.to_string()]
            return left_side_2, steps

            # # case a: mx + b
            # if isinstance(self.right_function.addends[0], Multiply) and\
            #         isinstance(self.right_function.addends[1], Constant):
            #     # case i: mx
            #     if isinstance(self.right_function.addends[0].factors[0], Constant) and\
            #         isinstance(self.right_function.addends[0].factors[1], SimplePower):
            #     # case ii: xm
            #     elif isinstance(self.right_function.addends[0].factors[1], Constant) and\
            #         isinstance(self.right_function.addends[0].factors[0], SimplePower):
            #
            #     #case iii: neither
            #     else:
            #         return False
            # # case b: b + mx
            # elif isinstance(self.right_function.addends[1], Multiply) and\
            #         isinstance(self.right_function.addends[0], Constant):

        # case 3: Right side is constant
        # case 4: Neither side is constant

    def solve(self, var: Variable):
        # check for linearity
        if self.is_linear():
            return self.solve_linear()
        return None

    def to_string(self):
        return self.left_function.to_string() + " = " + self.right_function.to_string()
