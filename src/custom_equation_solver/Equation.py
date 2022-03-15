from Function import Function
from Variable import Variable

class Equation:
    def __init__(self, leftFunction, rightFunction):
        self.leftFunction = leftFunction
        self.rightFunction = rightFunction

    def solve(self, var: Variable):
        return var
