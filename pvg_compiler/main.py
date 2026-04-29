# pvg_compiler/main.py
import sys
import os
import pprint
from lexer import PVGLexer
from parser import PVGParser
from generator import SVGGenerator

def compile_pvg(input_path, output_path, print_ast=False):
    if not os.path.exists(input_path):
        print(f"Błąd: Plik '{input_path}' nie istnieje.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()

    print(f"⚙️  Kompilacja pliku: {input_path}")
    
    lexer = PVGLexer()
    tokens = lexer.tokenize(code)

    parser = PVGParser()
    ast = parser.parse(tokens)

    if not ast:
        print("❌ Błąd składniowy przerwał kompilację.")
        return

    if print_ast:
        print("\n🌳 Wygenerowane Drzewo Składniowe (AST):")
        pprint.pprint(ast)
        print("-" * 40)

    generator = SVGGenerator()
    svg_output = generator.generate(ast)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_output)

    print(f"✅ Sukces! Wygenerowano plik: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Użycie: python main.py <plik.pvg> [opcje]")
        print("Przykład: python main.py examples/03_funkcje_i_matematyka.pvg --ast")
        sys.exit(1)

    input_file = sys.argv[1]
    
    base_name = os.path.basename(input_file).split('.')[0]
    output_file = os.path.join("output", f"{base_name}.svg")
    
    show_ast = "--ast" in sys.argv

    compile_pvg(input_file, output_file, print_ast=show_ast)