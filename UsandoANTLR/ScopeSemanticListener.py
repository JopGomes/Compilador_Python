from GrammarListener import GrammarListener
from SemanticChecker import SemanticChecker
from SymbolTable import SymbolTable

class ScopeSemanticListener(GrammarListener):
    def __init__(self):
        self.current_scope = SymbolTable()  
        self.scopes = [self.current_scope]  
        self.semantic_checker = SemanticChecker()

    def enterProgram(self, ctx):
        print("Entering global scope.")
    
    def exitProgram(self, ctx):
        print("Exiting global scope.")
        print(self.current_scope)
        if self.semantic_checker.has_errors():
            self.semantic_checker.report_errors()
        else:
            print("No semantic errors found.")

    def enterDf(self, ctx):
        function_name = ctx.idd().getText()
        print(f"Entering function scope: {function_name}")
        self.current_scope.define(function_name, "function")

        new_scope = SymbolTable(self.current_scope)
        self.current_scope = new_scope
        self.scopes.append(new_scope)

    def exitDf(self, ctx):
        print(f"Exiting function scope.")
        self.scopes.pop()
        self.current_scope = self.scopes[-1]

    def enterDv(self, ctx):
        if ctx.t() and ctx.li():
            var_name = ctx.li().getText()
            var_type = ctx.t().getText()
            print(f"Defining variable: {var_name} of type {var_type}")
            self.current_scope.define(var_name, var_type)
        else:
            print("exitDF:",ctx)

    def enterDt(self, ctx):
        type_name = ctx.idd().getText()
        type_definition = ctx.t().getText()
        print(f"Defining type: {type_name} = {type_definition}")
        self.current_scope.define(type_name, "type")

    def enterLv(self, ctx):
        var_name = ctx.getText()
        try:
            symbol = self.current_scope.resolve(var_name)
            print(f"Accessing variable: {var_name} -> {symbol}")
        except Exception as e:
            self.semantic_checker.add_error(str(e))

    def enterIdd(self, ctx):
        identifier = ctx.getText()
        try:
            symbol = self.current_scope.resolve(identifier)
            print(f"Using identifier: {identifier} -> {symbol}")
        except Exception as e:
            self.semantic_checker.add_error(str(e))

    def enterE(self, ctx):
        if ctx.getChildCount() == 1:
            left = ctx.getChild(0)  # Exemplo de chamada para visitar
        else:

            left = ctx.e(0)  # lado esquerdo
            right = ctx.e(1)  # lado direito
            if left and right:
                left_type = self.get_expression_type(left)
                right_type = self.get_expression_type(right)
                if left_type != right_type:
                    self.semantic_checker.add_error(f"Type mismatch in expression: {left_type} != {right_type}")
    
    def get_expression_type(self, ctx):
        if ctx.NUM():
            return 'integer'
        elif ctx.TRUE() or ctx.FALSE():
            return 'boolean'
        elif ctx.CHR():
            return 'char'
        elif ctx.STR():
            return 'string'
        elif ctx.idu():
            identifier = ctx.idu().getText()
            try:
                symbol = self.current_scope.resolve(identifier)
                return symbol.type
            except Exception as e:
                self.semantic_checker.add_error(str(e))
        return None

    def enterFunctionCall(self, ctx):
        function_name = ctx.idu().getText()
        try:
            function_symbol = self.current_scope.resolve(function_name)
            if function_symbol.type != 'function':
                self.semantic_checker.add_error(f"{function_name} is not a function.")
            else:
                print(f"Calling function {function_name}")
                num_args = len(ctx.le().e())  # Número de argumentos passados
                expected_params = 2  # Supondo que a função espera 2 parâmetros
                if num_args != expected_params:
                    self.semantic_checker.add_error(f"Function {function_name} expects {expected_params} arguments but got {num_args}")
        except Exception as e:
            self.semantic_checker.add_error(str(e))
