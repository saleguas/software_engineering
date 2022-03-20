from abc import ABC


class Function(ABC):
    var = ""

    def evaluate(self, x: float):
        pass

    def is_linear(self):
        pass

    def to_string(self):
        pass
