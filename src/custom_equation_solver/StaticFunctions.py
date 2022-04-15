import string

from Multiply import Multiply
from Add import Add
from Constant import Constant
from SimplePower import SimplePower
# from Equation import Equation
from Variable import Variable


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
            for i in range(len(function.addends)):
                if isinstance(function.addends[i], Add):
                    new_factors = []
                    for addend in function.addends[i].addends:
                        new_factors.append(addend)
                    function.addends.pop(i)
                    for addend in new_factors:
                        function.addends.append(addend)
                    i = 0

    return function


def standardize_linear_format(function):
    if not function.is_linear():
        return function
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


# def is_float(input: str):
#     # no double negatives allowed
#     negative = False
#     for i in range(len(input)):
#         if input[i] == "-" and i != 0:
#             return False


def is_float(number: str) -> bool:
    try:
        float(number)
        return True
    except ValueError:
        return False


def balanced_delimiters(input: str) -> bool:
    delimiter_count = 0
    for c in input:
        if c == "(":
            delimiter_count += 1
        elif c == ")":
            delimiter_count -= 1
        if delimiter_count < 0:
            return False
    return delimiter_count == 0


def parse_string(input: str):
    # don't filter numbers
    lowercase_letters = set(string.ascii_lowercase)
    uppercase_letters = set(string.ascii_uppercase)
    numbers = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    letters = lowercase_letters.union(uppercase_letters)
    allowed_symbols = {'*', '+', '-', '/', '^', '=', '(', ')', '.'}
    allowed_characters = allowed_symbols.union(letters).union(numbers)
    variable_name = ""
    variable_set = False
    # first remove invalid characters
    filtered_input = ""
    for c in input:
        if c in allowed_characters:
            filtered_input += c
        if c in letters:
            # make sure only one variable is used
            if not variable_set:
                variable_set = True
                variable_name = c
            else:
                assert c == variable_name
    # now get string for each side of the equation
    left_string = ""
    right_string = ""
    equals_passed = False
    for c in filtered_input:
        if c == "=":
            assert not equals_passed
            equals_passed = True
        elif not equals_passed:
            left_string += c
        else:
            right_string += c
    assert len(left_string) >= 1 and len(right_string) >= 1
    from Equation import Equation
    return Equation(parse_function(left_string), parse_function(right_string))


def parse_function(input: str):
    assert len(input) >= 1
    # remove unnecessary parentheses surround the whole string
    if input[0] == '(' and input[len(input) - 1] == ')' and balanced_delimiters(input[1:len(input) - 1]):
        return parse_function(input[1:len(input) - 1])
    # check for addition and subtraction not in parentheses
    # 2D arrays of format [index, isAddition]
    addition_indexes = []
    delimiter_count = 0
    for i in range(len(input)):
        if input[i] == '(':
            delimiter_count += 1
        elif input[i] == ')':
            delimiter_count -= 1
        elif input[i] == "+" and delimiter_count == 0:
            addition_indexes.append([i, True])
        # make sure this is subtraction and not negative sign
        elif input[i] == "-" and delimiter_count == 0 and i >= 1 and not input[i - 1].isnumeric():
            addition_indexes.append([i, False])
    assert delimiter_count == 0
    # check for multiplication and division
    # 2D arrays of format [index, isMultiplication]
    multiplication_indexes = []
    for i in range(len(input)):
        if input[i] == '(':
            delimiter_count += 1
        elif input[i] == ')':
            delimiter_count -= 1
        elif input[i] == "*" and delimiter_count == 0:
            multiplication_indexes.append([i, True])
        elif input[i] == "/" and delimiter_count == 0:
            multiplication_indexes.append([i, False])
    # check for exponents
    exponent_indexes = []
    for i in range(len(input)):
        if input[i] == '(':
            delimiter_count += 1
        elif input[i] == ')':
            delimiter_count -= 1
        elif input[i] == "^" and delimiter_count == 0:
            exponent_indexes.append(i)

    if is_float(input):
        return Constant(float(input))
    # separate by addition and subtraction if applicable
    elif len(addition_indexes) > 0:
        addends_string = []
        previous_index = -1
        for index_array in addition_indexes:
            addend = input[previous_index + 1:index_array[0]]
            assert len(addend) != 0
            previous_index = index_array[0]
            if not index_array[1]:
                addend = '-' + addend
            addends_string.append(addend)
        addends_string.append(input[previous_index + 1:len(input)])
        addend_functions = [parse_function(add) for add in addends_string]
        return Add([add for add in addend_functions])
    # separate by multiplication and division if applicable
    elif len(multiplication_indexes) > 0:
        factors_string = []
        previous_index = -1
        for index_array in multiplication_indexes:
            factor = input[previous_index + 1:index_array[0]]
            assert len(factor) != 0
            previous_index = index_array[0]
            if not index_array[1]:
                factor = '-' + factor
            factors_string.append(factor)
        factors_string.append(input[previous_index + 1:len(input)])
        multiply_functions = [parse_function(f) for f in factors_string]
        return Multiply([m for m in multiply_functions])
    # find exponents
    elif len(exponent_indexes) > 0:
        # Note: doesn't work for multiple exponentiation (like x^2^5)
        return SimplePower(Variable(input[0:exponent_indexes[0]]),
                           Constant(float(input[exponent_indexes[0] + 1:len(input)])))
    for a in input:
        if a.isnumeric():
            assert False
    # what is left must be a variable
    return SimplePower(Variable(input), Constant(1))


def get_quadratic_coefficients(function):
    a, b, c = 0, 0, 0
    if isinstance(function, SimplePower):
        assert function.power == 2
        a = Constant(1)
    elif isinstance(function, Multiply):
        assert len(function.factors) == 2
        for factor in function.factors:
            if isinstance(factor, Constant):
                a = factor
            else:
                assert isinstance(factor, SimplePower)
                assert factor.power == 2
    else:
        assert isinstance(function, Add)
        for addend in function.addends:
            if isinstance(addend, SimplePower):
                if addend.power == 1:
                    b = Constant(1)
                else:
                    assert addend.power == 2
                    a = Constant(1)
            elif isinstance(addend, Constant):
                c = addend
            else:
                assert isinstance(addend, Multiply)
                assert len(addend.factors) == 2
                if isinstance(addend.factors[0], Constant):
                    assert isinstance(addend.factors[1], SimplePower)
                    if addend.factors[1].power == 1:
                        b = addend.factors[0]
                    else:
                        assert addend.factors[1].power == 2
                        a = addend.factors[0]
                else:
                    assert isinstance(addend.factors[0], SimplePower)
                    assert isinstance(addend.factors[1], Constant)
                    if addend.factors[0].power == 1:
                        b = addend.factors[1]
                    else:
                        assert addend.factors[0].power == 2
                        a = addend.factors[1]
    return a, b, c
