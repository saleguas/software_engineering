# make a basic flask app
import os, sys
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "custom_equation_solver"))
sys.path.append(os.path.join(os.path.dirname(__file__), "templates"))


from equation_solver import solve_equation

# make a streamlit app
st.title("Equation Solver")
st.write("This is a simple equation solver")

# make a text input
equation = st.text_input("Enter your equation here")
# make a button
if st.button("Solve"):
    # solve the equation
    solution = solve_equation(equation)
    # display the solution
    st.write(solution)