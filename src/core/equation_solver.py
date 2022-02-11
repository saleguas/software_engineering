from sympy import *


def preprocess_equation(eq):
    for i in range(1, len(eq)):
        # check if there is a number right before a variable and replace it with a symbol
        if eq[i].isalpha() and eq[i-1].isdigit():
            # add an asterik between
            eq = eq[:i] + "*" + eq[i:]

    return sympify("Eq(" + eq.replace("=", ",") + ")")

def solve_equation(eq):
    try:
        if "=" in eq:
            valid_eq = preprocess_equation(eq)
            print(valid_eq)
            return solveset(valid_eq)
        else:
            return sympify(eq)
    except:
        return None
