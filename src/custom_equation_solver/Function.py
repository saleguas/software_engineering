from abc import ABC


"""def distribute(function):
    if isinstance(function, Multiply):
        for factor in function.factors:
            if isinstance(factor, Add):
                other_factors = [f for f in function.factors if f != factor]
                new_addends = []
                for addend in factor.addends:
                    new_factors = other_factors
                    new_factors.append(addend)
                    new_multiply = Multiply(new_factors)
                    new_addends.append(new_multiply)
                return distribute(Add(new_addends))
    elif isinstance(function, Add):
        for addend in function.addends:
            return distribute(addend)"""


class Function(ABC):
    # var = ""

    def evaluate(self, x: float):
        pass

    def is_linear(self):
        pass

    def to_string(self):
        pass

    def simplify(self):
        pass

