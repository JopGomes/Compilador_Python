from GrammarListener import GrammarListener
from SemanticChecker import SemanticChecker
from SymbolTable import SymbolTable

class ScopeSemanticListener(GrammarListener):
    def __init__(self):
        self.current_scope = SymbolTable()  # Global scope
        self.scopes = [self.current_scope]  # Stack para escopos aninhados
        self.semantic_checker = SemanticChecker()

    def enterProgram(self, ctx):
        """Entra no escopo global."""
        print("Entering global scope.")
    
    def exitProgram(self, ctx):
        """Sai do escopo global e reporta erros, se houver."""
        print("Exiting global scope.")
        print(self.current_scope)
        if self.semantic_checker.has_errors():
            self.semantic_checker.report_errors()
        else:
            print("No semantic errors found.")

    def enterDf(self, ctx):
        """Entra no escopo de uma função."""
        function_name = ctx.idd().getText()
        print(f"Entering function scope: {function_name}")
        self.current_scope.define(function_name, "function")

        # Cria um novo escopo para a função
        new_scope = SymbolTable(self.current_scope)
        self.current_scope = new_scope
        self.scopes.append(new_scope)

    def exitDf(self, ctx):
        """Sai do escopo da função."""
        print(f"Exiting function scope.")
        self.scopes.pop()
        self.current_scope = self.scopes[-1]

    def enterDv(self, ctx):
        """Declaração de variável."""
        if ctx.t() and ctx.li():
            var_name = ctx.li().getText()
            var_type = ctx.t().getText()
            print(f"Defining variable: {var_name} of type {var_type}")
            self.current_scope.define(var_name, var_type)
        else:
            print("exitDF:",ctx)

    def enterDt(self, ctx):
        """Declaração de tipo."""
        type_name = ctx.idd().getText()
        type_definition = ctx.t().getText()  # Captura o tipo definido
        print(f"Defining type: {type_name} = {type_definition}")
        self.current_scope.define(type_name, "type")

    def enterLv(self, ctx):
        """Acesso a uma variável e verificação de escopo."""
        var_name = ctx.getText()
        try:
            symbol = self.current_scope.resolve(var_name)
            print(f"Accessing variable: {var_name} -> {symbol}")
        except Exception as e:
            self.semantic_checker.add_error(str(e))

    def enterIdd(self, ctx):
        """Uso de identificador (Id) para variáveis e funções."""
        identifier = ctx.getText()
        try:
            symbol = self.current_scope.resolve(identifier)
            print(f"Using identifier: {identifier} -> {symbol}")
        except Exception as e:
            self.semantic_checker.add_error(str(e))

    def enterE(self, ctx):
        """Verificação de expressão (checagem de tipos)."""
        # Exemplo de verificação semântica de tipo de expressão
        if ctx.getChildCount() == 1:
            # Se apenas uma expressão estiver presente, não tente acessar com índice
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
        """Determina o tipo de uma expressão com base no contexto."""
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
        """Verificação de chamada de função (verifica se a função existe e se os argumentos estão corretos)."""
        function_name = ctx.idu().getText()
        try:
            function_symbol = self.current_scope.resolve(function_name)
            if function_symbol.type != 'function':
                self.semantic_checker.add_error(f"{function_name} is not a function.")
            else:
                print(f"Calling function {function_name}")
                # Verificar a correspondência de argumentos e parâmetros
                num_args = len(ctx.le().e())  # Número de argumentos passados
                # Aqui você poderia verificar o número de parâmetros da função, se armazenado
                # Exemplo:
                expected_params = 2  # Supondo que a função espera 2 parâmetros
                if num_args != expected_params:
                    self.semantic_checker.add_error(f"Function {function_name} expects {expected_params} arguments but got {num_args}")
        except Exception as e:
            self.semantic_checker.add_error(str(e))
