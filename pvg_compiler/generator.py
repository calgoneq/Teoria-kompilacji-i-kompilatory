# pvg_compiler/generator.py
import math

class SVGGenerator:
    def __init__(self):
        self.canvas_w = 800
        self.canvas_h = 600
        self.bg_color = "#ffffff"
        self.curr_color = "#000000"
        self.curr_stroke_w = 1
        self.curr_opacity = 1.0
        
        self.variables = {}
        self.functions = {}
        self.svg_elements = []

    def generate(self, ast):
        """Główna metoda uruchamiająca generowanie"""
        self.visit(ast)
        return self._build_svg_string()

    def _build_svg_string(self):
        """Skleja wszystkie tagi w pełny plik SVG"""
        lines = [
            f'<svg width="{self.canvas_w}" height="{self.canvas_h}" xmlns="http://www.w3.org/2000/svg">',
            f'    <rect width="100%" height="100%" fill="{self.bg_color}" />'
        ]
        for el in self.svg_elements:
            lines.append(f'    {el}')
        lines.append('</svg>')
        return "\n".join(lines)

    def visit(self, node):
        """Rekurencyjnie odwiedza węzły AST"""
        if not isinstance(node, tuple):
            return node

        kind = node[0]

        if kind == 'PROGRAM':
            for stmt in node[1]:
                self.visit(stmt)

        # --- USTAWIENIA PŁÓTNA I STANU ---
        elif kind == 'CANVAS':
            self.canvas_w = self.visit(node[1])
            self.canvas_h = self.visit(node[2])
        elif kind == 'BACKGROUND':
            self.bg_color = node[1].strip('"')
        elif kind == 'COLOR':
            self.curr_color = node[1].strip('"')
        elif kind == 'STROKE_WIDTH':
            self.curr_stroke_w = self.visit(node[1])
        elif kind == 'OPACITY':
            self.curr_opacity = self.visit(node[1])

        # --- KSZTAŁTY ---
        elif kind == 'CIRCLE':
            cx, cy, r = self.visit(node[1]), self.visit(node[2]), self.visit(node[3])
            self.svg_elements.append(
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{self.curr_color}" fill-opacity="{self.curr_opacity}" />'
            )
        elif kind == 'RECT':
            x, y, w, h = self.visit(node[1]), self.visit(node[2]), self.visit(node[3]), self.visit(node[4])
            self.svg_elements.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{self.curr_color}" fill-opacity="{self.curr_opacity}" />'
            )
        elif kind == 'LINE':
            x1, y1, x2, y2 = self.visit(node[1]), self.visit(node[2]), self.visit(node[3]), self.visit(node[4])
            self.svg_elements.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{self.curr_color}" stroke-width="{self.curr_stroke_w}" opacity="{self.curr_opacity}" />'
            )

        # --- ZMIENNE I WYRAŻENIA MATEMATYCZNE ---
        elif kind == 'NUMBER':
            return float(node[1]) if '.' in str(node[1]) else int(node[1])
        elif kind == 'VAR':
            if node[1] not in self.variables:
                print(f"[Ostrzeżenie] Niezainicjalizowana zmienna: {node[1]}, przyjmuję 0")
                return 0
            return self.variables[node[1]]
        elif kind == 'ASSIGN':
            val = self.visit(node[2])
            self.variables[node[1]] = val
            return val
        elif kind == 'BINOP':
            op, left, right = node[1], self.visit(node[2]), self.visit(node[3])
            if op == '+': return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/': return left / right if right != 0 else 0
            elif op == '%': return left % right if right != 0 else 0
            elif op == '==': return left == right
            elif op == '!=': return left != right
            elif op == '<': return left < right
            elif op == '>': return left > right
            elif op == '<=': return left <= right
            elif op == '>=': return left >= right
            elif op == 'and': return left and right
            elif op == 'or': return left or right

        elif kind == 'MATH_FUNC':
            func, arg = node[1], self.visit(node[2])
            if func == 'sin': return math.sin(math.radians(arg))
            elif func == 'cos': return math.cos(math.radians(arg))
            elif func == 'sqrt': return math.sqrt(arg)

        # --- KONTROLA PRZEPŁYWU (PĘTLE I IF) ---
        elif kind == 'IF':
            condition = self.visit(node[1])
            if condition:
                for stmt in node[2]: self.visit(stmt)
            else:
                for stmt in node[3]: self.visit(stmt)
                
        elif kind == 'WHILE':
            while self.visit(node[1]):
                for stmt in node[2]: self.visit(stmt)
                
        elif kind == 'FOR':
            self.visit(node[1])
            while self.visit(node[2]):
                for stmt in node[4]: self.visit(stmt)
                self.visit(node[3]) 

        # --- FUNKCJE PROCEDURALNE ---
        elif kind == 'DEF':
            self.functions[node[1]] = (node[2], node[3])
            
        elif kind == 'CALL':
            func_name, args = node[1], node[2]
            if func_name not in self.functions:
                print(f"[Błąd] Wywołanie nieznanej funkcji: {func_name}")
                return
            
            params, body = self.functions[func_name]
            
            old_vars = self.variables.copy()
            for param_name, arg_expr in zip(params, args):
                self.variables[param_name] = self.visit(arg_expr)
                
            for stmt in body:
                self.visit(stmt)
                
            self.variables = old_vars