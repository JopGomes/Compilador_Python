class SemanticError(Exception):
    pass

class SemanticChecker:
    def __init__(self):
        self.errors = []

    def add_error(self, message):
        self.errors.append(message)

    def has_errors(self):
        return len(self.errors) > 0

    def report_errors(self):
        number_err = 0
        for error in self.errors:
            print(f"Semantic Error {number_err} =>  {error}")
            number_err += 1
