from Function import Function


# DO NOT INSTANTIATE
class Variable(str, Function):
    def evaluate(self, x: float):
        return x
