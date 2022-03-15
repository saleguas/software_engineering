from Function import Function


class Constant(Function, float):
    def evaluate(self, x: float):
        return self
