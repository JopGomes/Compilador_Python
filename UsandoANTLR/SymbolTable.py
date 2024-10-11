class Symbol:
    def __init__(self, name, symbol_type):
        self.name = name
        self.type = symbol_type

    def __repr__(self):
        return f"{self.name}:{self.type}"

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent  

    def define(self, name, symbol_type):
        if name in self.symbols:
            raise Exception(f"Error: Symbol {name} already defined in this scope.")
        self.symbols[name] = Symbol(name, symbol_type)

    def resolve(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.resolve(name)
        else:
            raise Exception(f"Error: Symbol {name} not defined.")

    def __repr__(self):
        return f"Symbols: {self.symbols}"
