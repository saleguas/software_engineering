from collections import deque

# make class InputParser that will accept a mathematical expression and return a list of tokens following the order of the operators and operands
class InputParser:

    def __init__(self, input_str=None):
        self.input_str = input_str
        self.tokens = deque()
        self.operators = ['+', '-', '*', '/', '^']
        self.valid_variables = 'abcdefghijklmnopqrstuvwxyz'
        self.priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '()': 100}

    def parse(self):
        if self.input_str is None:
            raise ValueError('Input string is empty')
        else:
            self.input_str = self.input_str.replace(' ', '')
            self.input_str = self.input_str.replace('\n', '')

            # check if we need to solve for a variable
            if "=" in self.input_str:
                self.input_str = self.input_str.split('=')




#  3x + 5 = 2
# (x + 3) * 5 = 2