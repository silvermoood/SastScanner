class SymbolTable:
    def __init__(self):
        self.tainted = set()

    def mark_tainted(self, name):
        self.tainted.add(name)

    def is_tainted(self, name):
        return name in self.tainted
