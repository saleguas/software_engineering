import sys, os

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('..'))

from src.app import app
from src.core import equation_solver

def test_preprocess_equation():
    res1 = equation_solver.solve_equation('3x = 9')
    res2 = equation_solver.solve_equation('3+3')
    res3 = equation_solver.solve_equation('3/4x = 9')

    assert res1.args[0] == 3
    assert res2 == 6
    assert res3.args[0] == 12

def test_showing_valid_result():
    test_equation = '3x = 9'
    tester = app.test_client()
    response = tester.post(
      '/',
      data = dict(equation=test_equation, result=equation_solver.solve_equation(test_equation)),
      follow_redirects=True
      )
    assert b'{3}' in response.data

