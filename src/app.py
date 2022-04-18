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
# make a streamlit app
st.title("Equation Solver")
st.write("This is a simple equation solver")

# make a text input
equation = st.text_input("Enter your equation here")
# make a button
if st.button("Solve"):
    # solve the equation
    solution, steps = None, None
    try:
        equation = parse_string(equation)
        if equation.is_linear():
            solution, steps = equation.solve_linear()
        elif equation.is_quadratic():
            solution, steps = equation.solve_quadratic()
        else:
            solution = solve_equation(equation)
            # display the solution
    except:
        solution = solve_equation(equation)
    st.markdown("### Solution: " + str(solution))
    if steps == None:
        st.markdown("No steps currently supported for this equation")
    else:
        st.markdown("## Steps:")
        for step in steps:
            st.markdown(step)