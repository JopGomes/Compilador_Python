from antlr4 import *
from GrammarLexer import GrammarLexer
from GrammarParser import GrammarParser
from ScopeSemanticListener import ScopeSemanticListener

def main():

    #file_path = input("Enter the path to the source code file: ")
    file_path= "input.txt"
    with open(file_path, 'r') as file:
        input_stream = InputStream(file.read())

    lexer = GrammarLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = GrammarParser(token_stream)

    tree = parser.program()


    scope_and_semantic_listener = ScopeSemanticListener()
    walker = ParseTreeWalker()
    walker.walk(scope_and_semantic_listener, tree)

if __name__ == '__main__':
    main()

