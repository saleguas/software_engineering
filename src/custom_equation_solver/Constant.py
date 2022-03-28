from Function import Function


class Constant(Function, float):
    def evaluate(self, x: float):
        return self

    def is_linear(self):
        return True

    def to_string(self):
        return str(self)

    def simplify(self):
        return self
