from Function import Function
from SimplePower import SimplePower
from Multiply import Multiply
from Constant import Constant


class Add(Function):
    """
    A class to represent addition of functions

    ...
    Attributes
    ----------
    addends : list
        store addends

    Methods
    -------
    __init__(addends):
        initialize the equation with a left function and a right function
    evaluate(x):
        evaluate the function at a given point
    combine_like_terms():
        combine like terms
    simplify():
        simplify addends by combining like terms, removing zeros, and calling simplify on products
    is_quadratic():
        check whether the function is quadratic
    is_linear():
        check whether the function is linear
    to_string():
        return the string representation of the function
    """

    def __init__(self, addends=None):
        """initialize addends to the input; make addends None otherwise"""
        if not isinstance(addends, list):
            self.addends = []
        else:
            self.addends = addends

    def evaluate(self, x: float):
        """return the value of the function at a given point, x"""
        sum = 0
        for f in self.addends:
            sum += f.evaluate(x)
        return sum

    def combine_like_terms(self):
        """modify addends to combine like terms"""
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
                                                                  (isinstance(addend, Multiply) and len(addend.factors) == 2 and (
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
                self.addends.append(SimplePower(term[0], Constant(term[1])))
            elif terms[term] != 0:
                self.addends.append(Multiply([Constant(terms[term]), SimplePower(term[0], Constant(term[1]))]))

    def simplify(self):
        """simplify addends by combining like terms, removing zeros, and calling simplify on products"""
        self.combine_like_terms()

        self.addends = [a for a in self.addends if a != 0]

        for addend in self.addends:
            if isinstance(addend, Multiply):
                addend.simplify()

    def is_linear(self):
        """return whether each addend is linear"""
        for addend in self.addends:
            if not addend.is_linear():
                return False
        return True

    def is_quadratic(self):
        """return whether each addend is quadratic"""
        for addend in self.addends:
            if not addend.is_quadratic():
                return False
        return True

    def to_string(self):
        """return the string representation of the sum"""
        string = ""
        for i in range(len(self.addends)):
            string += self.addends[i].to_string()
            if i != len(self.addends) - 1:
                string += " + "
        return string
