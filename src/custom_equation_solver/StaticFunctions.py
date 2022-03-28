from Multiply import Multiply
from Add import Add


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
