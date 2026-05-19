# pvg_compiler/parser.py
from sly import Parser
from lexer import PVGLexer

class PVGParser(Parser):
    def __init__(self):
        super().__init__()
        self.has_error = False
        self.source_code = ""
        
    tokens = PVGLexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', EQ, NE, '<', '>', LE, GE),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', NOT),
        ('right', 'UMINUS'),
    )

    @_('statements')
    def program(self, p): return ('PROGRAM', p.statements)

    @_('statements statement', 'statement')
    def statements(self, p):
        return p.statements + [p.statement] if len(p) == 2 else [p.statement]

    @_('simple_statement ";"')
    def statement(self, p): return p.simple_statement

    @_('if_statement', 'for_statement', 'while_statement', 'def_statement')
    def statement(self, p): return p[0]

    # PĘTLE I WARUNKI
    @_('IF "(" expr ")" "{" statements "}"')
    def if_statement(self, p): return ('IF', p.expr, p.statements, [])

    @_('IF "(" expr ")" "{" statements "}" ELSE "{" statements "}"')
    def if_statement(self, p): return ('IF', p.expr, p.statements0, p.statements1)

    @_('WHILE "(" expr ")" "{" statements "}"')
    def while_statement(self, p): return ('WHILE', p.expr, p.statements)

    @_('FOR "(" simple_statement ";" expr ";" simple_statement ")" "{" statements "}"')
    def for_statement(self, p): return ('FOR', p.simple_statement0, p.expr, p.simple_statement1, p.statements)

    @_('DEF IDENT "(" params ")" "{" statements "}"')
    def def_statement(self, p): return ('DEF', p.IDENT, p.params, p.statements)

    # INSTRUKCJE PROSTE
    @_('BREAK', 'CONTINUE')
    def simple_statement(self, p): return (p[0].upper(),)

    @_('PRINT "(" expr ")"')
    def simple_statement(self, p): return ('PRINT', p.expr)

    @_('LET IDENT "=" expr')
    def simple_statement(self, p): return ('ASSIGN', p.IDENT, p.expr)

    @_('IDENT "=" expr')
    def simple_statement(self, p): return ('ASSIGN', p.IDENT, p.expr)

    # TABLICE
    @_('LET IDENT "=" "[" array_items "]"')
    def simple_statement(self, p): return ('ASSIGN_ARRAY', p.IDENT, p.array_items)

    @_('IDENT "[" expr "]" "=" expr')
    def simple_statement(self, p): return ('SET_ARRAY', p.IDENT, p.expr0, p.expr1)

    @_('IDENT "(" args ")"')
    def simple_statement(self, p): return ('CALL', p.IDENT, p.args)

    # KANWA
    @_('CANVAS "(" expr "," expr ")"')
    def simple_statement(self, p): return ('CANVAS', p.expr0, p.expr1)

    @_('BACKGROUND "(" expr ")"')
    def simple_statement(self, p): return ('BACKGROUND', p.expr)

    # GRAFIKA
    @_('FILL "(" expr ")" ')
    def simple_statement(self, p): return ('FILL', p.expr)

    @_('STROKE "(" expr ")" ')
    def simple_statement(self, p): return ('STROKE', p.expr)

    @_('STROKE_WIDTH "(" expr ")" ')
    def simple_statement(self, p): return ('STROKE_WIDTH', p.expr)

    @_('OPACITY "(" expr ")" ')
    def simple_statement(self, p): return ('OPACITY', p.expr)

    @_('FONT_SIZE "(" expr ")" ')
    def simple_statement(self, p): return ('FONT_SIZE', p.expr)

    @_('FONT_FAMILY "(" expr ")" ')
    def simple_statement(self, p): return ('FONT_FAMILY', p.expr)

    # TRANSFORMACJE
    @_('ROTATE "(" expr ")"')
    def simple_statement(self, p): return ('ROTATE', p.expr)

    @_('TRANSLATE "(" expr "," expr ")"')
    def simple_statement(self, p): return ('TRANSLATE', p.expr0, p.expr1)

    @_('SCALE "(" expr "," expr ")"')
    def simple_statement(self, p): return ('SCALE', p.expr0, p.expr1)

    # KSZTAŁTY
    @_('CIRCLE "(" expr "," expr "," expr ")"')
    def simple_statement(self, p): return ('CIRCLE', p.expr0, p.expr1, p.expr2)

    @_('RECT "(" expr "," expr "," expr "," expr ")"')
    def simple_statement(self, p): return ('RECT', p.expr0, p.expr1, p.expr2, p.expr3)

    @_('LINE "(" expr "," expr "," expr "," expr ")"')
    def simple_statement(self, p): return ('LINE', p.expr0, p.expr1, p.expr2, p.expr3)

    @_('ELLIPSE "(" expr "," expr "," expr "," expr ")"')
    def simple_statement(self, p): return ('ELLIPSE', p.expr0, p.expr1, p.expr2, p.expr3)

    @_('POLYGON "(" expr ")"')
    def simple_statement(self, p): return ('POLYGON', p.expr)

    @_('POLYLINE "(" expr ")"')
    def simple_statement(self, p): return ('POLYLINE', p.expr)

    @_('PATH "(" expr ")"')
    def simple_statement(self, p): return ('PATH', p.expr)

    @_('TEXT_CMD "(" expr "," expr "," expr ")"')
    def simple_statement(self, p): return ('TEXT', p.expr0, p.expr1, p.expr2)

    # WYRAŻENIA
    @_('expr "+" expr', 'expr "-" expr', 'expr "*" expr', 'expr "/" expr', 'expr "%" expr',
       'expr EQ expr', 'expr NE expr', 'expr "<" expr', 'expr ">" expr',
       'expr LE expr', 'expr GE expr', 'expr AND expr', 'expr OR expr')
    def expr(self, p): return ('BINOP', p[1], p.expr0, p.expr1)

    @_('NOT expr')
    def expr(self, p): return ('NOT', p.expr)

    @_('"-" expr %prec UMINUS')
    def expr(self, p): return ('UNARY', '-', p.expr)

    @_('"(" expr ")"')
    def expr(self, p): return p.expr

    @_('IDENT')
    def expr(self, p): return ('VAR', p.IDENT)
    
    @_('IDENT "[" expr "]"')
    def expr(self, p): return ('GET_ARRAY', p.IDENT, p.expr)

    @_('INT', 'FLOAT')
    def expr(self, p): return ('NUMBER', p[0])

    @_('STRING')
    def expr(self, p): return ('STRING', p[0].strip('"'))

    # FUNKCJE MATEMATYCZNE
    @_('SIN "(" expr ")"', 'COS "(" expr ")"', 'TAN "(" expr ")"', 
       'SQRT "(" expr ")"', 'LOG "(" expr ")"', 'EXP "(" expr ")"', 
       'ABS "(" expr ")"', 'ROUND "(" expr ")"', 'CEIL "(" expr ")"', 'FLOOR "(" expr ")" ')
    def expr(self, p): return ('MATH_FUNC', p[0], p.expr)

    # LISTY I PARAMETRY
    @_('array_items "," expr', 'expr')
    def array_items(self, p): return p[0] + [p[2]] if len(p) == 3 else [p[0]]
    @_('empty')
    def array_items(self, p): return []

    @_('params "," IDENT', 'IDENT')
    def params(self, p): return p[0] + [p[2]] if len(p) == 3 else [p[0]]
    @_('empty')
    def params(self, p): return []

    @_('args "," expr', 'expr')
    def args(self, p): return p[0] + [p[2]] if len(p) == 3 else [p[0]]
    @_('empty')
    def args(self, p): return []

    @_('')
    def empty(self, p): pass

    def error(self, p):
        self.has_error = True
        if p:
            print(f"❌ BŁĄD SKŁADNIOWY (Syntax Error)")
            print(f"Napotkano niespodziewany element: '{p.value}' (Typ: {p.type}) w linii {p.lineno}")
            
            if self.source_code:
                lines = self.source_code.split('\n')
                if p.lineno <= len(lines):
                    print(f"-> {lines[p.lineno - 1].strip()}")
        else:
            print("\n❌ BŁĄD SKŁADNIOWY: Nieoczekiwany koniec pliku (brakuje nawiasu lub średnika?).\n")

if __name__ == '__main__':
    lexer = PVGLexer()
    parser = PVGParser()
    text = '''
    let napis = "Witaj";
    let tablica = [1, 2, 3];
    fill("#ff0000");
    text(100, 100, napis);
    polygon("10,10 20,20 30,10");
    '''
    import pprint
    pprint.pprint(parser.parse(lexer.tokenize(text)))