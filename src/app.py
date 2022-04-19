# make a basic streamlit app
import os, sys
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "custom_equation_solver"))
sys.path.append(os.path.join(os.path.dirname(__file__), "templates"))


from equation_solver import solve_equation
from StaticFunctions import *
from Equation import Equation
from sympy import *
# make a streamlit app
st.title("Wolfram Omicron Delta - Equation Solver")
st.write("Enter an equation below to view the solution and steps.")
st.caption("Note: use an asterisk to indicate multiplication")
# make a text input
in_equation = st.text_input("Enter your equation here")
# make a button
if st.button("Solve"):
    # solve the equation
    print(in_equation)
    solution, steps = None, None
    try:
        test_equation = parse_string(in_equation)
        equation = parse_string(in_equation)
        # simplify test_equation to see if it is linear
        for i in range(20):
            test_equation.left_function = distribute(test_equation.left_function)
            test_equation.right_function = distribute(test_equation.right_function)
            test_equation.left_function = remove_nesting(test_equation.left_function)
            test_equation.right_function = remove_nesting(test_equation.right_function)
            test_equation.left_function.simplify()
            test_equation.right_function.simplify()
        # if the simplified version of the equation is linear, then it can be solved with solve_linear
        if test_equation.is_linear():
            solution, steps = equation.solve_linear()
        # if the simplified version of the equation is quadratic, then it can be solved with solve_quadratic
        elif test_equation.is_quadratic():
            solution, steps = equation.solve_quadratic()
        # solve the equation with SymPy
        if solve_equation(in_equation) != None:
            solution = latex(solve_equation(in_equation))
            # display the solution
    except Exception as e:
        print(e)
        solution = latex(solve_equation(equation))
    st.latex(solution)
    if steps == None:
        st.markdown("No steps currently supported for this equation")
    else:
        st.markdown("## Steps:")
        for step in steps:
            for j in range(0, len(step), 80):
                st.text(step[j:min(j+80, len(step))])
            st.text("")