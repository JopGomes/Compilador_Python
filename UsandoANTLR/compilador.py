import sys
from antlr4 import *
from GrammarLexer import GrammarLexer
from GrammarParser import GrammarParser
from ScopeSemanticListener import ScopeSemanticListener
from CodeGeneratorListener import CodeGeneratorListener
from CodeGeneratorAssembly import CodeGeneratorAssembly

import subprocess
import os

def compile_c_code(c_file_name, output_executable_name="a.out"):
    if not os.path.exists(c_file_name):
        print(f"Error: {c_file_name} not found!")
        return

    compile_command = f"gcc {c_file_name} -o {output_executable_name}"

    try:
        result = subprocess.run(compile_command, shell=True, check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        print(f"Compilation failed with error: {e.stderr}")



def main():
    # input_stream = FileStream(input("Enter the path to the source code file: "))
    file_path = "../UsandoANTLR/input.txt"
    with open(file_path, 'r') as file:
        input_stream = InputStream(file.read())


    lexer = GrammarLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = GrammarParser(token_stream)

    tree = parser.program()

    scope_listener = ScopeSemanticListener()
    walker = ParseTreeWalker()
    walker.walk(scope_listener, tree)

    # Geração de executavel C
    code_listener = CodeGeneratorListener()
    walker.walk(code_listener, tree)

    code_listener.get_code_output()

    c_file_name = "output.c"
    output_executable_name = "output_c"  # Nome do executável gerado

    compile_c_code(c_file_name, output_executable_name)

    # Geração de código Assembly
    code_listener_assembly = CodeGeneratorAssembly()
    walker.walk(code_listener_assembly, tree)

    code_listener_assembly.get_code_output() 

if __name__ == '__main__':
    main()
