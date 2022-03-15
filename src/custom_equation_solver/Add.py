from Function import Function
from SimplePower import SimplePower
from Multiply import Multiply
from Constant import Constant


class Add(Function):
    def __init__(self, addends=None):
        if not isinstance(addends, list):
            self.addends = []
        else:
            self.addends = addends

    def evaluate(self, x: float):
        sum = 0
        for f in self.addends:
            sum += f.evaluate(x)
        return sum

    def combine_like_terms(self):
        # combine constants
        constants = []
        for addend in self.addends:
            if isinstance(addend, int) or isinstance(addend, float):
                constants.append(addend)
        # delete constants from self.addends
        self.addends = [addend for addend in self.addends if not (isinstance(addend, int) or isinstance(addend, float))]
        # determine new constant and append it to self.addends
        new_constant = 0
        for constant in constants:
            new_constant += constant
        self.addends.append(Constant(new_constant))

        # combine non-constant like terms
        terms = {}
        for addend in self.addends:
            # add 1 to coefficient if there is a simple power
            if isinstance(addend, SimplePower):
                if (addend.base, addend.power) in terms:
                    terms[(addend.base, addend.power)] += 1
                else:
                    terms[(addend.base, addend.power)] = 1
            # add to coefficient if Multiply has exclusively a constant and a simple power
            elif isinstance(addend, Multiply):
                if len(addend.factors) == 2:
                    if (isinstance(addend.factors[0], int) or isinstance(addend.factors[0], float)) and \
                            isinstance(addend.factors[1], SimplePower):
                        if (addend.factors[1].base, addend.factors[1].power) in terms:
                            terms[(addend.factors[1].base, addend.factors[1].power)] += addend.factors[0]
                        else:
                            terms[(addend.factors[1].base, addend.factors[1].power)] = addend.factors[0]
                    elif (isinstance(addend.factors[1], int) or isinstance(addend.factors[1], float)) and \
                            isinstance(addend.factors[0], SimplePower):
                        if (addend.factors[0].base, addend.factors[0].power) in terms:
                            terms[(addend.factors[0].base, addend.factors[0].power)] += addend.factors[1]
                        else:
                            terms[(addend.factors[0].base, addend.factors[0].power)] = addend.factors[1]

        # delete simple power functions and multiply functions with constant * power
        self.addends = [addend for addend in self.addends if not (isinstance(addend, SimplePower) or
                                                                  (isinstance(addend, Multiply) and (
                                                                              ((isinstance(addend.factors[0], int) or
                                                                                isinstance(addend.factors[0],
                                                                                           float)) and
                                                                               isinstance(addend.factors[1],
                                                                                          SimplePower)) or
                                                                              ((isinstance(addend.factors[1], int) or
                                                                                isinstance(addend.factors[1], float))
                                                                               and isinstance(addend.factors[0],
                                                                                              SimplePower)))))]

        # append simplified power functions.
        for term in terms:
            if terms[term] == 1:
                self.addends.append(SimplePower(term[0], term[1]))
            else:
                self.addends.append(Multiply([Constant(terms[term]), SimplePower(term[0], term[1])]))

    def simplify(self):
        self.combine_like_terms()
