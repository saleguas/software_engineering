from Function import Function
from Variable import Variable
from Constant import Constant
from Add import Add
from Multiply import Multiply
from SimplePower import SimplePower
from StaticFunctions import *


class Equation:
    """
    A class to represent equations

    ...
    Attributes
    ----------
    left_function : Function
        function on the left side of the equation
    right_function : Function
        function on the right side of the equation

    Methods
    -------
    __init__(left_function, right_function):
        initialize the equation with a left function and a right function
    is_quadratic():
        check whether the equation is quadratic
    solve_quadratic():
        assuming the equation is quadratic, solve it like a quadratic equation
    is_linear():
        check whether the equation is linear
    solve_linear():
        assuming the equation is linear, solve it like a linear equation
    to_string():
        return the string representation of the equation
    """

    def __init__(self, left_function: Function, right_function: Function):
        """Initialize the equation to have functions on the left and right side"""
        self.left_function = left_function
        self.right_function = right_function

    def is_quadratic(self):
        """Return whether each side of the equation is quadratic"""
        return self.left_function.is_quadratic() and self.right_function.is_quadratic()

    def solve_quadratic(self):
        """Return the solutions and explanations for a quadratic equation"""

        # store the steps to solve the equation (list of strings)
        steps = []

        # apply distributive property
        self.left_function = distribute(self.left_function)
        self.right_function = distribute(self.right_function)
        steps.append("If applicable, apply the distributive property, yielding " + self.to_string() + ".")

        # simplify the equation as much as possible
        self.left_function = remove_nesting(self.left_function)
        self.right_function = remove_nesting(self.right_function)
        self.left_function.simplify()
        self.right_function.simplify()
        for i in range(20):
            self.left_function = distribute(self.left_function)
            self.right_function = distribute(self.right_function)
            self.left_function = remove_nesting(self.left_function)
            self.right_function = remove_nesting(self.right_function)
            self.left_function.simplify()
            self.right_function.simplify()

        # move all terms to the left side, leaving just 0 on the right
        self.left_function = Add([self.left_function, Multiply([Constant(-1), self.right_function])])
        self.right_function = Constant(0)
        steps.append(
            "Move everything to the left side, yielding " + self.left_function.to_string() + " = " + self.right_function.to_string() + ".")

        # simplify the left side, if possible
        for i in range(20):
            self.left_function = distribute(self.left_function)
            self.left_function = remove_nesting(self.left_function)
            self.left_function.simplify()

        # make the left side 0 if the addends add to 0
        if isinstance(self.left_function, Add) and len(self.left_function.addends) == 0:
            self.left_function = Constant(0)
        # add step to indicate that the equation was simplified
        steps.append("Simplify: " + self.to_string() + ".")
        assert self.left_function.is_quadratic()
        # if the simplifications resulted in a linear equation, solve the equation as a linear equation
        if self.left_function.is_linear():
            steps.append("This is now a linear equation, so solve it like a linear equation.")
            solution, linear_steps = self.solve_linear()
            for step in linear_steps:
                steps.append(step)
            return solution, steps
        # The equation is quadratic and not linear, so a is not 0. Thus, the quadratic formula applies.
        # Get the coefficients of each term with a being the quadratic coefficient, b being the linear coefficient,
        # and c being the constant.
        a, b, c = get_quadratic_coefficients(self.left_function)
        solution = ((-b + (b ** 2 - 4 * a * c) ** .5) / (2 * a), (-b - (b ** 2 - 4 * a * c) ** .5) / (2 * a))
        steps.append("Use the quadratic formula. The quadratic formula is (-b +- sqrt(b^2-4ac))/(2a) with a=" + str(a) +
                     ", b=" + str(b) + ", c= " + str(c) + ".")
        return solution, steps

    def is_linear(self):
        """Return whether both sides of the equation are linear"""
        return self.left_function.is_linear() and self.right_function.is_linear()

    # Returns the solution or true or false is there are infinitely many or no solutions
    def solve_linear(self):
        """Assuming the equation is linear, solve it. Return solution and explanation."""
        # Store steps
        steps = []
        # Simplify (distribute and combine like terms)
        self.left_function = distribute(self.left_function)
        self.right_function = distribute(self.right_function)
        steps.append(
            "If applicable, apply the distributive property, yielding " + self.left_function.to_string() + " = " + \
            self.right_function.to_string())
        self.left_function = remove_nesting(self.left_function)
        self.right_function = remove_nesting(self.right_function)
        self.left_function.simplify()
        self.right_function.simplify()
        for i in range(20):
            self.left_function = distribute(self.left_function)
            self.right_function = distribute(self.right_function)
            self.left_function = remove_nesting(self.left_function)
            self.right_function = remove_nesting(self.right_function)
            self.left_function.simplify()
            self.right_function.simplify()
        # write the equation in the form ax+b=cx+d
        self.left_function = standardize_linear_format(self.left_function)
        self.right_function = standardize_linear_format(self.right_function)
        steps.append("If applicable, simplify, yielding " + self.left_function.to_string() + " = " + \
                     self.right_function.to_string())

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
            left_side_2 = left_side_1 / slope
            steps += ["Subtract " + constant.to_string() + " from both sides of the equation, yielding " +
                      self.left_function.to_string() + " - " + constant.to_string() + " = " +
                      self.right_function.to_string() + " - " + constant.to_string() + ".",
                      "Simplify: " + str(left_side_1) + " = " + slope.to_string() + "*" + variable.to_string() + ".",
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
            steps += ["Subtract " + constant.to_string() + " from both sides of the equation, yielding " +
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
            slope_difference = Constant(float(slope_left - slope_right))
            constant_difference = Constant(float(constant_right - constant_left))
            left_side_1 = Add([Multiply([slope_difference, variable_right]), constant_left])
            right_side_1 = constant_right
            left_side_2 = Multiply([slope_difference, variable_right])
            right_side_2 = constant_difference
            steps += ["Subtract " + slope_right.to_string() + "*" + variable_right + " from both sides of the equation, yielding " +
                     self.left_function.to_string() + " - " + slope_right.to_string() + "*" + variable_right + " = " +
                     self.right_function.to_string() + " - " + slope_right.to_string() + "*" + variable_right + ".",
                     "Simplify: " + left_side_1.to_string() + " = " + str(right_side_1) + ".",
                     "Subtract " + str(constant_left) + " from both side of the equation, yielding " +
                     left_side_1.to_string() + " - " + str(constant_left) + " = " + right_side_1.to_string() + " - " +
                     str(constant_left) + ".",
                     "Simplify: " + left_side_2.to_string() + " = " + right_side_2.to_string() + ".",
                     "Divide both sides by " + str(slope_difference) + ": " +
                     "(" + slope_difference.to_string() + variable_right.to_string() + ")/" + slope_difference.to_string() + " = " +
                     constant_difference.to_string() + "/" + slope_difference.to_string() + ".",
                     "Simplify: " + variable_right.to_string() + " = " + str(constant_difference/slope_difference)]
            solution = Constant(float(constant_difference/slope_difference))
            return solution, steps

    def to_string(self):
        """Return the string representation of the equation."""
        return self.left_function.to_string() + " = " + self.right_function.to_string()
