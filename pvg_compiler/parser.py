# pvg_compiler/parser.py
from sly import Parser
from lexer import PVGLexer

class PVGParser(Parser):
    tokens = PVGLexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', EQ, NE, '<', '>', LE, GE),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    @_('statements')
    def program(self, p):
        return ('PROGRAM', p.statements)

    @_('statements statement', 'statement')
    def statements(self, p):
        if len(p) == 2:
            return p.statements + [p.statement]
        return [p.statement]

    @_('simple_statement ";"')
    def statement(self, p):
        return p.simple_statement

    @_('if_statement', 'for_statement', 'while_statement', 'def_statement')
    def statement(self, p):
        return p[0]

    # --- LISTA PRODUKCJI (INSTURKCJE PROSTE) ---
    @_('CANVAS "(" expr "," expr ")"')
    def simple_statement(self, p): return ('CANVAS', p.expr0, p.expr1)

    @_('BACKGROUND "(" STRING ")"')
    def simple_statement(self, p): return ('BACKGROUND', p.STRING)

    @_('COLOR "(" STRING ")"')
    def simple_statement(self, p): return ('COLOR', p.STRING)

    @_('STROKE_WIDTH "(" expr ")"')
    def simple_statement(self, p): return ('STROKE_WIDTH', p.expr)

    @_('OPACITY "(" expr ")"')
    def simple_statement(self, p): return ('OPACITY', p.expr)

    @_('CIRCLE "(" expr "," expr "," expr ")"')
    def simple_statement(self, p): return ('CIRCLE', p.expr0, p.expr1, p.expr2)

    @_('RECT "(" expr "," expr "," expr "," expr ")"')
    def simple_statement(self, p): return ('RECT', p.expr0, p.expr1, p.expr2, p.expr3)

    @_('LINE "(" expr "," expr "," expr "," expr ")"')
    def simple_statement(self, p): return ('LINE', p.expr0, p.expr1, p.expr2, p.expr3)

    @_('ELLIPSE "(" expr "," expr "," expr "," expr ")"')
    def simple_statement(self, p): return ('ELLIPSE', p.expr0, p.expr1, p.expr2, p.expr3)

    @_('LET IDENT "=" expr')
    def simple_statement(self, p): return ('ASSIGN', p.IDENT, p.expr)

    @_('IDENT "=" expr')
    def simple_statement(self, p): return ('ASSIGN', p.IDENT, p.expr)

    @_('PRINT "(" expr ")"')
    def simple_statement(self, p): return ('PRINT', p.expr)

    @_('IDENT "(" args ")" ')
    def simple_statement(self, p): return ('CALL', p.IDENT, p.args)

    # --- KONSTRUKCJE ZŁOŻONE ---
    @_('IF "(" expr ")" "{" statements "}" [ ELSE "{" statements "}" ]')
    def if_statement(self, p):
        return ('IF', p.expr, p.statements0, p.statements1 if p.statements1 else [])

    @_('WHILE "(" expr ")" "{" statements "}"')
    def while_statement(self, p):
        return ('WHILE', p.expr, p.statements)

    @_('FOR "(" simple_statement ";" expr ";" simple_statement ")" "{" statements "}"')
    def for_statement(self, p):
        return ('FOR', p.simple_statement0, p.expr, p.simple_statement1, p.statements)

    @_('DEF IDENT "(" params ")" "{" statements "}"')
    def def_statement(self, p):
        return ('DEF', p.IDENT, p.params, p.statements)

    # --- WYRAŻENIA I FUNKCJE MATEMATYCZNE ---
    @_('expr "+" expr', 'expr "-" expr', 'expr "*" expr', 'expr "/" expr',
       'expr EQ expr', 'expr NE expr', 'expr "<" expr', 'expr ">" expr',
       'expr LE expr', 'expr GE expr', 'expr AND expr', 'expr OR expr')
    def expr(self, p): return ('BINOP', p[1], p.expr0, p.expr1)

    @_('SIN "(" expr ")"', 'COS "(" expr ")"', 'SQRT "(" expr ")"')
    def expr(self, p): return ('MATH_FUNC', p[0], p.expr)

    @_('"-" expr %prec UMINUS')
    def expr(self, p): return ('UNARY', '-', p.expr)

    @_('"(" expr ")"')
    def expr(self, p): return p.expr

    @_('IDENT')
    def expr(self, p): return ('VAR', p.IDENT)

    @_('INT', 'FLOAT')
    def expr(self, p): return ('NUMBER', p[0])

    # --- POMOCNICZE ---
    @_('params "," IDENT', 'IDENT')
    def params(self, p):
        return p[0] + [p[2]] if len(p) == 3 else [p[0]]

    @_('empty')
    def params(self, p): return []

    @_('args "," expr', 'expr')
    def args(self, p):
        return p[0] + [p[2]] if len(p) == 3 else [p[0]]

    @_('empty')
    def args(self, p): return []

    @_('')
    def empty(self, p): pass

    def error(self, p):
        if p: print(f"Błąd składniowy: {p.type} ('{p.value}') linia {p.lineno}")
        else: print("Błąd: Nieoczekiwany koniec pliku")

if __name__ == '__main__':
    lexer = PVGLexer()
    parser = PVGParser()
    text = '''
    canvas(1000, 1000);
    stroke_width(2);
    opacity(0.5);
    def kwiat(x, y) {
        color("#ff00ff");
        circle(x, y, 20);
        for (let i = 0; i < 360; i = i + 45) {
            line(x, y, x + sin(i)*50, y + cos(i)*50);
        }
    }
    if (sqrt(100) == 10) { kwiat(500, 500); }
    '''
    import pprint
    pprint.pprint(parser.parse(lexer.tokenize(text)))