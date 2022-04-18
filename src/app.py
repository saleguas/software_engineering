# make a basic flask app
import os, sys
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "custom_equation_solver"))
sys.path.append(os.path.join(os.path.dirname(__file__), "templates"))


from equation_solver import solve_equation
from StaticFunctions import parse_string
from Equation import Equation
from sympy import *
# make a streamlit app
st.title("Wolfram Omicron Delta - Equation Solver")
st.write("Enter an equation below to view the solution and steps.")
# make a text input
equation = st.text_input("Enter your equation here")
# make a button
if st.button("Solve"):
    # solve the equation
    print(equation)
    solution, steps = None, None
    try:
        equation = parse_string(equation)
        print(equation)
        if equation.is_linear():
            solution, steps = equation.solve_linear()
        elif equation.is_quadratic():
            solution, steps = equation.solve_quadratic()
        else:
            solution = latex(solve_equation(equation))
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
            st.write(step)