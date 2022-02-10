# make a basic flask app
import os, sys
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

sys.path.append(os.path.abspath('.'))

from core.equation_solver import solve_equation

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # get the input from the form
    equation = request.form.get('equation')
    data = {'equation': equation}
    print(equation)
    if equation != None:
        # solve the equation
        try:
            data['result'] = solve_equation(equation)
        except Exception as e:
            data['result'] = str(e)
    # return the result to the template
    print(data)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
