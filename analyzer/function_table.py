class FunctionSummary:
    def __init__(self):
        self.tainted_params = set()
        self.returns_tainted = False


class FunctionTable:
    def __init__(self):
        self.functions = {}

    def add_function(self, name):
        self.functions[name] = FunctionSummary()

    def get(self, name):
        return self.functions.get(name)
