from GrammarListener import GrammarListener
from GrammarParser import GrammarParser

class CodeGeneratorListener(GrammarListener):
    def __init__(self):
        self.code = []  # Lista que armazenará as linhas do código gerado
        self.indentation_level = 0  # Controle da indentação do código gerado

    def enterDf(self, ctx: GrammarParser.DfContext):
        # Começar a geração de código de uma função
        func_name = ctx.idd().getText()
        return_type = ctx.t().getText()
        params = self.generateParams(ctx)
        self.add_line(f"{return_type} {func_name}({params}) {{")
        self.indent()

    def exitDf(self, ctx: GrammarParser.DfContext):
        # Finalizar a função com a chave de fechamento
        self.unindent()
        self.add_line("}")

    def enterDv(self, ctx: GrammarParser.DvContext):
        # Gerar declaração de variáveis
        var_type = ctx.t().getText()
        var_names = self.generateVarList(ctx.li())
        self.add_line(f"{var_type} {var_names};")

    def enterS(self, ctx: GrammarParser.SContext):
        # Gerar atribuições
        var_name = ctx.lv().getText()
        expr = self.generateExpression(ctx.e())
        self.add_line(f"{var_name} = {expr};")

    def generateParams(self, ctx):
    # Geração de parâmetros da função (apenas um)
    
        while ctx.lp() is not None:
            param_name = ctx.lp().idd().getText() 
            param_type = ctx.lp().t().getText() if ctx.lp().t() is not None else "unknown"  
            
            return f"{param_type} {param_name}"  
        else:
            print("No parameters found in function definition.")
            return ""


    def generateVarList(self, ctx):
        # Geração de lista de variáveis
        vars = ctx.idd().getText()
        return vars

    def generateExpression(self, ctx):
        # Geração de expressões (recursiva)
        if ctx.getChildCount() == 1:
            return ctx.getText()  # Valor ou variável simples
        else:
            left = self.generateExpression(ctx.getChild(0))
            operator = ctx.getChild(1).getText()
            right = self.generateExpression(ctx.getChild(2))
            return f"{left} {operator} {right}"

    def indent(self):
        self.indentation_level += 1

    def unindent(self):
        self.indentation_level -= 1

    def add_line(self, line):
        # Adicionar uma linha de código com a indentação apropriada
        self.code.append("    " * self.indentation_level + line)

    def get_code(self):
        # Retornar o código gerado como uma string
        return "\n".join(self.code)

        
    def get_code_output(self):

        code = self.get_code()
        new_code =code.replace("integer", "int") # roubo por preguiça de mudar para int
        print("code:\n",new_code,self.code)

        with open("output.c", "w") as output_file:
            output_file.write(new_code)

        print("Code generated successfully in 'output.c'")
