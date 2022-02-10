from sympy import *

def preprocess_equation(eq):
    return "Eq(" + eq.replace("=", ",") + ")"

def solve_equation(eq):
    try:
        if "=" in eq:
            valid_eq = preprocess_equation(eq)
            print(valid_eq)
            return sympify(solve(valid_eq))
        else:
            return sympify(eq)
    except:
        return None
