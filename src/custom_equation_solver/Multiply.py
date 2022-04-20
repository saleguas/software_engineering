from Function import Function
from Constant import Constant
from SimplePower import SimplePower


class Multiply(Function):
    """
    A class to represent multiplication of functions

    ...
    Attributes
    ----------
    factors : list
        store the factors of the function

    Methods
    -------
    __init__(addends):
        initialize the function's factors, if any
    evaluate(x):
        evaluate the function at a given point
    remove_nested_multiply():
        modify factors so that it contains no multiply functions; they are redundant
    combine_constants():
        modify factors so that constants are multiplied together
    combine_powers():
        modify factors so that power functions with the same base are merged
    simplify():
        call removed_nested_multiply(), combine_constants(), and combine_powers()
    is_quadratic():
        check whether the function is quadratic
    is_linear():
        check whether the function is linear
    to_string():
        return the string representation of the function
    """

    def __init__(self, factors=None):
        """instantiate a Multiply object with input factors, if applicable"""
        if not isinstance(factors, list):
            self.factors = []
        else:
            self.factors = factors

    def evaluate(self, x: float):
        """evaluate at x by evaluating each function at x and multiplying them together"""
        product = 1
        for f in self.factors:
            product *= f.evaluate(x)
        return product

    # eliminate nested "multiply" functions
    def remove_nested_multiply(self):
        """if factors contains any multiply functions, add the factors of the multiply functions to self.factors
        and remove the multiply function contained in self"""
        new_factors = list()
        for factor in self.factors:
            if isinstance(factor, Multiply):
                factor.remove_nested_multiply()
                for inner_factor in factor.factors:
                    new_factors.append(inner_factor)
            else:
                new_factors.append(factor)
        self.factors = new_factors

    #combine constants
    def combine_constants(self):
        """multiply constants together"""
        # store constants in a list
        constants = list()
        for factor in self.factors:
            if isinstance(factor, int) or isinstance(factor, float):
                constants.append(factor)
        # remove constants from self.factors
        self.factors = [factor for factor in self.factors if
                        not isinstance(factor, int) and not isinstance(factor, float)]
        # determine new constant and insert it into self.factors
        new_constant = 1
        for constant in constants:
            new_constant *= constant
        new_constant = Constant(new_constant)
        self.factors.insert(0, new_constant)

    # combine power functions
    def combine_powers(self):
        """merge power functions with the same base"""
        # key: base; value: list of indexes of the powers for the given base
        power_bases = {}
        for i in range(len(self.factors)):
            # consider adding Power and/or Variable
            if isinstance(self.factors[i], SimplePower):
                if not self.factors[i].base in power_bases:
                    power_bases[self.factors[i].base] = [i]
                else:
                    power_bases[self.factors[i].base].append(i)
        # now, the value of power_bases will be the new power for each base
        for base in power_bases:
            total_power = 0
            for index in power_bases[base]:
                total_power += self.factors[index].power
            power_bases[base] = total_power
        # delete power functions in self.factors
        self.factors = [factor for factor in self.factors if not isinstance(factor, SimplePower)]
        # Insert new power functions
        for base in power_bases:
            self.factors.append(SimplePower(base, Constant(power_bases[base])))

    def simplify(self):
        """simplify by calling remove_nested_multiply(), combine_constants(), and combine_powers()"""
        # eliminate nested "multiply" functions
        self.remove_nested_multiply()

        # combine constants
        self.combine_constants()

        # combine powers
        self.combine_powers()

    def is_linear(self):
        """Check whether the multiply function is linear. A simplified Multiply function is linear if it is empty,
        its only factor is linear, or it is a Constant multiplied by a power and the power function is linear."""
        if len(self.factors) == 1:
            return self.factors[0].is_linear()
        if len(self.factors) == 2:
            if isinstance(self.factors[0], Constant) and isinstance(self.factors[1], SimplePower):
                return self.factors[1].is_linear()
            elif isinstance(self.factors[1], Constant) and isinstance(self.factors[0], SimplePower):
                return self.factors[0].is_linear()
        return len(self.factors) == 0

    def is_quadratic(self):
        """Check whether the function is quadratic. A simplified Multiply function is quadratic if it is empty,
        its only factor is quadratic, or it is a Constant multiply by a power function that is quadratic."""
        if len(self.factors) == 1:
            return self.factors[0].is_quadratic()
        if len(self.factors) == 2:
            if isinstance(self.factors[0], Constant) and isinstance(self.factors[1], SimplePower):
                return self.factors[1].is_quadratic()
            elif isinstance(self.factors[1], Constant) and isinstance(self.factors[0], SimplePower):
                return self.factors[0].is_quadratic()
        return len(self.factors) == 0

    def to_string(self):
        """return the string representation of the function"""
        string = ""
        from Add import Add
        for i in range(len(self.factors)):
            # Add parentheses if any factor is an add function; this is necessary to follow the order of operations
            if isinstance(self.factors[i], Add):
                string += '('
            string += self.factors[i].to_string()
            if isinstance(self.factors[i], Add):
                string += ')'
            if i != len(self.factors) - 1:
                string += "*"
        return string
