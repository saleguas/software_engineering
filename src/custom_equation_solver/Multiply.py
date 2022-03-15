from Function import Function
from Constant import Constant
from Variable import Variable
from SimplePower import SimplePower
from Exponential import Exponential


class Multiply(Function):
    def __init__(self, factors=None):
        if not isinstance(factors, list):
            self.factors = []
        else:
            self.factors = factors

    def evaluate(self, x: float):
        product = 1
        for f in self.factors:
            product *= f.evaluate(x)
        return product

    # eliminate nested "multiply" functions
    def remove_nested_multiply(self):
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
        # store constants in a list
        constants = list()
        for factor in self.factors:
            if isinstance(factor, int) or isinstance(factor, float):
                constants.append(factor)
        # remove constants from self.factors
        self.factors = [factor for factor in self.factors if
                        not isinstance(factor, int) and not isinstance(factor, float)]
        # factor_index = 0
        # while factor_index < len(self.factors):
        #     if isinstance(self.factors[factor_index], int) or isinstance(self.factors[factor_index], float):
        #         self.factors.pop(factor_index)

        # determine new constant and insert it into self.factors
        new_constant = Constant(1)
        for constant in constants:
            new_constant *= Constant(constant)
        self.factors.insert(0, new_constant)

    #combine power functions
    def combine_powers(self):
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
            self.factors.append(SimplePower(base, power_bases[base]))

    # Postconditions: constants are multiplied together, and functions
    # are ordered as follows: constant, variable or power (variable if power is 1;
    # both need not exist simultaneously in simplified function),
    # exponential
    def simplify(self):
        # eliminate nested "multiply" functions
        self.remove_nested_multiply()

        # combine constant
        self.combine_constants()

        # combine powers
        self.combine_powers()

