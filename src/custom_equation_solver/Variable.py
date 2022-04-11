from Function import Function


# DO NOT INSTANTIATE
class Variable(str, Function):
    def evaluate(self, x: float):
        return x

    def is_linear(self):
        return True

    def is_quadratic(self):
        return True

    def to_string(self):
        return self
