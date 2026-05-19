# pvg_compiler/main.py
import sys
import os
import pprint
from lexer import PVGLexer
from parser import PVGParser
from generator import SVGGenerator, SemanticError

def print_error_context(code, lineno, index=None, error_msg=""):
    lines = code.split('\n')
    error_line = lines[lineno - 1] if lineno <= len(lines) else ""
    
    print(f"❌ {error_msg}")
    print(f"  Linia {lineno}: {error_line.strip()}")
    if index is not None:
        col = index - sum(len(l) + 1 for l in lines[:lineno - 1])
        if col > 0:
            print("  " + " " * (col - len(error_line) + len(error_line.strip()) + 8) + "^")

def compile_pvg(input_path, output_path, print_ast=False):
    if not os.path.exists(input_path):
        print(f"Błąd: Plik '{input_path}' nie istnieje.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()

    print(f"⚙️  Kompilacja pliku: {input_path}")
    
    lexer = PVGLexer()
    lexer.source_code = code 
    tokens = list(lexer.tokenize(code))

    if lexer.has_error:
        print("❌ Analiza przerwana z powodu błędów leksykalnych.")
        return

    parser = PVGParser()
    parser.source_code = code
    ast = parser.parse(iter(tokens))

    if parser.has_error or not ast:
        print("❌ Kompilacja przerwana z powodu błędów składniowych.")
        return

    if print_ast:
        print("\n🌳 Wygenerowane Drzewo Składniowe (AST):")
        pprint.pprint(ast)
        print("-" * 40)

    try:
        generator = SVGGenerator()
        svg_output = generator.generate(ast)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_output)
        print(f"✅ Sukces! Wygenerowano plik: {output_path}")

    except SemanticError as e:
        print(f"🛑 BŁĄD SEMANTYCZNY: {str(e)}")
        print("❌ Kompilacja przerwana.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Użycie: python3 main.py <plik.pvg> [--ast]")
        sys.exit(1)

    input_file = sys.argv[1]
    base_name = os.path.basename(input_file).split('.')[0]
    output_file = os.path.join("output", f"{base_name}.svg")
    show_ast = "--ast" in sys.argv

    compile_pvg(input_file, output_file, print_ast=show_ast)