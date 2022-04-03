from Multiply import Multiply
from Add import Add
from Constant import Constant
from SimplePower import SimplePower


def distribute(function):
    if isinstance(function, Multiply):
        for factor in function.factors:
            if isinstance(factor, Add):
                other_factors = [f for f in function.factors if f != factor]
                new_addends = []
                for addend in factor.addends:
                    new_factors = other_factors.copy()
                    new_factors.append(addend)
                    new_multiply = Multiply(new_factors)
                    new_addends.append(new_multiply)
                return distribute(Add(new_addends))
    elif isinstance(function, Add):
        for i in range(len(function.addends)):
            function.addends[i] = distribute(function.addends[i])
    return function


def remove_nesting(function):
    if isinstance(function, Multiply):
        if len(function.factors) == 1:
            return function.factors[0]
        else:
            for i in range(len(function.factors)):
                function.factors[i] = remove_nesting(function.factors[i])
    if isinstance(function, Add):
        if len(function.addends) == 1:
            return function.addends[0]
        else:
            for i in range(len(function.addends)):
                function.addends[i] = remove_nesting(function.addends[i])
    return function


def standardize_linear_format(function):
    if not function.is_linear():
        return None
    if isinstance(function, Add):
        # return Add([standardize_linear_format(addend) for addend in function.addends])
        for i in range(len(function.addends)):
            if isinstance(function.addends[i], SimplePower):
                function.addends[i] = Multiply([function.addends[i], Constant(1)])
    if isinstance(function, Multiply) and len(function.factors) == 1:
        return Add([Multiply([function.factors[0], Constant(1)]), Constant(0)])
    if isinstance(function, Multiply) and len(function.factors) == 2:
        return Add([function, Constant(0)])
    if isinstance(function, SimplePower):
        return Add([Multiply([function, Constant(1)]), Constant(0)])

    return function
