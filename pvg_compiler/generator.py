# pvg_compiler/generator.py
import math

class BreakException(Exception): pass
class ContinueException(Exception): pass
class SemanticError(Exception): pass

class SVGGenerator:
    def __init__(self):
        self.canvas_w = 800
        self.canvas_h = 600
        self.bg_color = "#ffffff"
        self.curr_fill = "#000000"
        self.curr_stroke = "none"
        self.curr_stroke_w = 1
        self.curr_opacity = 1.0
        self.curr_font_size = 16
        self.curr_font_family = "Arial"
        self.curr_transform = ""
        
        self.variables = {}
        self.functions = {}
        self.svg_elements = []

    def generate(self, ast):
        self.visit(ast)
        return self._build_svg_string()

    def _build_svg_string(self):
        lines = [
            f'<svg width="{self.canvas_w}" height="{self.canvas_h}" xmlns="http://www.w3.org/2000/svg">',
            f'    <rect width="100%" height="100%" fill="{self.bg_color}" />'
        ]
        for el in self.svg_elements: lines.append(f'    {el}')
        lines.append('</svg>')
        return "\n".join(lines)

    def _get_style(self):
        return f'fill="{self.curr_fill}" stroke="{self.curr_stroke}" stroke-width="{self.curr_stroke_w}" opacity="{self.curr_opacity}" transform="{self.curr_transform}"'

    def visit(self, node):
        if not isinstance(node, tuple): return node
        kind = node[0]

        if kind == 'PROGRAM':
            for stmt in node[1]: self.visit(stmt)

        # Ustawienia i Atrybuty
        elif kind == 'CANVAS':
            self.canvas_w, self.canvas_h = self.visit(node[1]), self.visit(node[2])
        elif kind == 'BACKGROUND': self.bg_color = self.visit(node[1])
        elif kind == 'FILL': self.curr_fill = self.visit(node[1])
        elif kind == 'STROKE': self.curr_stroke = self.visit(node[1])
        elif kind == 'STROKE_WIDTH': self.curr_stroke_w = self.visit(node[1])
        elif kind == 'OPACITY': self.curr_opacity = self.visit(node[1])
        elif kind == 'FONT_SIZE': self.curr_font_size = self.visit(node[1])
        elif kind == 'FONT_FAMILY': self.curr_font_family = self.visit(node[1])
        elif kind == 'ROTATE': self.curr_transform += f' rotate({self.visit(node[1])})'
        elif kind == 'TRANSLATE': self.curr_transform += f' translate({self.visit(node[1])},{self.visit(node[2])})'
        elif kind == 'SCALE': self.curr_transform += f' scale({self.visit(node[1])},{self.visit(node[2])})'

        # Kształty
        elif kind == 'CIRCLE':
            cx, cy, r = self.visit(node[1]), self.visit(node[2]), self.visit(node[3])
            self.svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" {self._get_style()} />')
        elif kind == 'RECT':
            x, y, w, h = self.visit(node[1]), self.visit(node[2]), self.visit(node[3]), self.visit(node[4])
            self.svg_elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {self._get_style()} />')
        elif kind == 'LINE':
            x1, y1, x2, y2 = self.visit(node[1]), self.visit(node[2]), self.visit(node[3]), self.visit(node[4])
            self.svg_elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{self.curr_fill}" stroke-width="{self.curr_stroke_w}" opacity="{self.curr_opacity}" transform="{self.curr_transform}" />')
        elif kind == 'ELLIPSE':
            cx, cy, rx, ry = self.visit(node[1]), self.visit(node[2]), self.visit(node[3]), self.visit(node[4])
            self.svg_elements.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" {self._get_style()} />')
        elif kind == 'POLYGON':
            pts = self.visit(node[1])
            self.svg_elements.append(f'<polygon points="{pts}" {self._get_style()} />')
        elif kind == 'POLYLINE':
            pts = self.visit(node[1])
            self.svg_elements.append(f'<polyline points="{pts}" {self._get_style()} fill="none" stroke="{self.curr_fill}" />')
        elif kind == 'PATH':
            d = self.visit(node[1])
            self.svg_elements.append(f'<path d="{d}" {self._get_style()} />')
        elif kind == 'TEXT':
            x, y, text = self.visit(node[1]), self.visit(node[2]), self.visit(node[3])
            self.svg_elements.append(f'<text x="{x}" y="{y}" font-family="{self.curr_font_family}" font-size="{self.curr_font_size}" {self._get_style()}>{text}</text>')

        # Zmienne, tablice i print
        elif kind == 'PRINT': print(self.visit(node[1]))
        elif kind == 'NUMBER': return float(node[1]) if '.' in str(node[1]) else int(node[1])
        elif kind == 'STRING': return str(node[1])
        elif kind == 'VAR':
            if node[1] not in self.variables:
                raise SemanticError(f"Próba użycia niezadeklarowanej zmiennej: '{node[1]}'")
            return self.variables[node[1]]
        elif kind == 'ASSIGN':
            val = self.visit(node[2])
            self.variables[node[1]] = val
            return val
        elif kind == 'ASSIGN_ARRAY':
            self.variables[node[1]] = [self.visit(i) for i in node[2]]
        elif kind == 'GET_ARRAY':
            if node[1] not in self.variables:
                raise SemanticError(f"Tablica '{node[1]}' nie istnieje.")
            
            idx = int(self.visit(node[2]))
            tablica = self.variables[node[1]]
            
            if idx < 0 or idx >= len(tablica):
                raise SemanticError(f"Próba odczytu spoza zakresu. Tablica '{node[1]}' ma długość {len(tablica)}, a zażądano indeksu {idx}.")
            return tablica[idx]
        elif kind == 'SET_ARRAY':
            idx, val = int(self.visit(node[2])), self.visit(node[3])
            self.variables[node[1]][idx] = val

        # Operatory i matematyka
        elif kind == 'NOT': return not self.visit(node[1])
        elif kind == 'UNARY': return -self.visit(node[2])
        elif kind == 'BINOP':
            op, left, right = node[1], self.visit(node[2]), self.visit(node[3])

            if op == '/' and right == 0:
                raise SemanticError("Dzielenie przez zero jest niedozwolone!")
            if op == '%' and right == 0:
                raise SemanticError("Modulo przez zero jest niedozwolone!")

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
            elif func == 'tan': return math.tan(math.radians(arg))
            elif func == 'sqrt': return math.sqrt(arg)
            elif func == 'log': return math.log(arg)
            elif func == 'exp': return math.exp(arg)
            elif func == 'abs': return abs(arg)
            elif func == 'round': return round(arg)
            elif func == 'ceil': return math.ceil(arg)
            elif func == 'floor': return math.floor(arg)

        # Kontrola przepływu
        elif kind == 'BREAK': raise BreakException()
        elif kind == 'CONTINUE': raise ContinueException()
        
        elif kind == 'IF':
            if self.visit(node[1]):
                for stmt in node[2]: self.visit(stmt)
            else:
                for stmt in node[3]: self.visit(stmt)
                
        elif kind == 'WHILE':
            while self.visit(node[1]):
                try:
                    for stmt in node[2]: self.visit(stmt)
                except BreakException: break
                except ContinueException: continue
                
        elif kind == 'FOR':
            self.visit(node[1])
            while self.visit(node[2]):
                try:
                    for stmt in node[4]: self.visit(stmt)
                except BreakException: break
                except ContinueException: pass
                self.visit(node[3])

        # Funkcje
        elif kind == 'DEF':
            self.functions[node[1]] = (node[2], node[3])
            
        elif kind == 'CALL':
            func_name, args = node[1], node[2]
            
            if func_name not in self.functions: 
                raise SemanticError(f"Próba wywołania nieistniejącej procedury: '{func_name}()'")
                
            params, body = self.functions[func_name]
            
            if len(args) != len(params):
                raise SemanticError(f"Procedura '{func_name}' wymaga {len(params)} argumentów, a podano {len(args)}.")
                
            old_vars = self.variables.copy()
            for p_name, a_expr in zip(params, args):
                self.variables[p_name] = self.visit(a_expr)
            for stmt in body: self.visit(stmt)
            self.variables = old_vars