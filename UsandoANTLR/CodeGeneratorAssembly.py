from GrammarListener import GrammarListener
from GrammarParser import GrammarParser

class CodeGeneratorAssembly(GrammarListener):
    def __init__(self):
        self.code = []  
        self.label_count = 0  
        self.stack_pointer = 0  

    def enterDf(self, ctx: GrammarParser.DfContext):
        
        func_name = ctx.idd().getText()
        self.add_line(f"{func_name}:")  
        self.add_line("push ebp")  
        self.add_line("mov ebp, esp")  
        self.stack_pointer = 0

    def exitDf(self, ctx: GrammarParser.DfContext):
        self.add_line("mov esp, ebp")  
        self.add_line("pop ebp") 
        self.add_line("ret")  

    def enterDv(self, ctx: GrammarParser.DvContext):
        var_type = ctx.t().getText()
        var_name = ctx.li().getText()
        self.stack_pointer += 4  
        self.add_line(f"sub esp, 4  ;")

    def enterS(self, ctx: GrammarParser.SContext):
        if ctx.lv() is not None and ctx.e() is not None:
            var_name = ctx.lv().getText()
            expr = self.generateExpression(ctx.e())
            self.add_line(expr)  
            self.add_line(f"mov [ebp-{self.stack_pointer}], eax  ; ")

    def generateParams(self, ctx):
        if ctx.lp() is not None:
            param_name = ctx.lp().idd().getText()
            self.add_line(f"push {param_name}  ; ")
        else:
            print("No parameters found in function definition.")
            return ""
    
    def generateIf(self, ctx):
        label_true = self.new_label()
        label_end = self.new_label()

        condition_code = self.generateExpression(ctx.e(0))  # Assume que a primeira expressão é a condição
        self.add_line(condition_code)
        self.add_line("cmp eax, 0  ;")
        self.add_line(f"jne {label_true}  ; ")

        # Bloco else (caso exista)
        if ctx.getChildCount() > 2:  # Verifica se há um bloco else
            self.generateStatement(ctx.getChild(2))
        self.add_line(f"jmp {label_end}  ;")

        self.add_line(f"{label_true}:")
        # Bloco then (caso exista)
        self.generateStatement(ctx.getChild(1))
        self.add_line(f"{label_end}:")

    def generateWhile(self, ctx):
        label_start = self.new_label()
        label_end = self.new_label()

        self.add_line(f"{label_start}:")
        condition_code = self.generateExpression(ctx.e(0))  # Assume que a primeira expressão é a condição
        self.add_line(condition_code)
        self.add_line("cmp eax, 0  ;")
        self.add_line(f"je {label_end}  ;")

        # Corpo do loop
        self.generateStatement(ctx.getChild(1))  # Assume que o corpo do loop é o segundo filho
        self.add_line(f"jmp {label_start}  ;")
        self.add_line(f"{label_end}:")

    def generateExpression(self, ctx):
        if ctx.getChildCount() == 1:
            return f"mov eax, {ctx.getText()}  ;"
        else:
            left = self.generateExpression(ctx.getChild(0))
            operator = ctx.getChild(1).getText()
            right = self.generateExpression(ctx.getChild(2))

            self.add_line(left) 
            self.add_line("push eax")  
            self.add_line(right)  
            self.add_line("pop ebx")  

            if operator == "+":
                return "add eax, ebx  ; "
            elif operator == "-":
                return "sub eax, ebx  ; "
            elif operator == "*":
                return "imul eax, ebx  ; "
            elif operator == "/":
                return "xor edx, edx  ; \nidiv ebx  ; "
            else:
                return f"Unsupported operator {operator}"

    def add_line(self, line):
        self.code.append(line)

    def get_code(self):
        return "\n".join(self.code)

    def get_code_output(self):
        code = self.get_code()
        print("Generated Assembly Code:\n", code)

        with open("output.asm", "w") as output_file:
            output_file.write(code)

