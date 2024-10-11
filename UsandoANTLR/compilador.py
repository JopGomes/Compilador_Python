import sys
from antlr4 import *
from GrammarLexer import GrammarLexer
from GrammarParser import GrammarParser
from ScopeSemanticListener import ScopeSemanticListener
from CodeGeneratorListener import CodeGeneratorListener

def main():
    # Leitura do arquivo de entrada
    # input_stream = FileStream(input("Enter the path to the source code file: "))
    file_path = "input.txt"
    with open(file_path, 'r') as file:
        input_stream = InputStream(file.read())


    # Inicialização do lexer e parser
    lexer = GrammarLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = GrammarParser(token_stream)

    # Construção da árvore de análise
    tree = parser.program()

    # Caminho da análise semântica e escopo
    scope_listener = ScopeSemanticListener()
    walker = ParseTreeWalker()
    walker.walk(scope_listener, tree)

    # Geração de código
    code_listener = CodeGeneratorListener()
    walker.walk(code_listener, tree)

    # Exibição do código gerado
    code_listener.get_code_output()

if __name__ == '__main__':
    main()
