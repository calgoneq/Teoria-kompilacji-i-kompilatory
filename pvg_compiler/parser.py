from sly import Parser
from lexer import PVGLexer

class PVGParser(Parser):
    tokens = PVGLexer.tokens

    precedence = (
        ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )


    @_('statements')
    def program(self, p):
        return ('PROGRAM', p.statements)

    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_('simple_statement ";"')
    def statement(self, p):
        return p.simple_statement

    @_('if_statement', 'for_statement', 'while_statement', 'def_statement')
    def statement(self, p):
        return p[0]

    @_('CANVAS "(" expr "," expr ")" ')
    def simple_statement(self, p):
        return ('CANVAS', p.expr0, p.expr1)

    @_('BACKGROUND "(" STRING ")" ')
    def simple_statement(self, p):
        return ('BACKGROUND', p.STRING)

    @_('COLOR "(" STRING ")" ')
    def simple_statement(self, p):
        return ('COLOR', p.STRING)

    @_('CIRCLE "(" expr "," expr "," expr ")" ')
    def simple_statement(self, p):
        return ('CIRCLE', p.expr0, p.expr1, p.expr2)

    @_('RECT "(" expr "," expr "," expr "," expr ")" ')
    def simple_statement(self, p):
        return ('RECT', p.expr0, p.expr1, p.expr2, p.expr3)

    @_('LET IDENT "=" expr')
    def simple_statement(self, p):
        return ('ASSIGN', p.IDENT, p.expr)

    @_('IDENT "(" args ")" ')
    def simple_statement(self, p):
        return ('CALL', p.IDENT, p.args)

    @_('DEF IDENT "(" params ")" "{" statements "}" ')
    def def_statement(self, p):
        return ('DEF', p.IDENT, p.params, p.statements)

    @_('FOR "(" simple_statement ";" expr ";" simple_statement ")" "{" statements "}" ')
    def for_statement(self, p):
        return ('FOR', p.simple_statement0, p.expr, p.simple_statement1, p.statements)

    @_('params "," IDENT', 'args "," expr')
    def params(self, p): return p[0] + [p[2]]
    
    @_('IDENT', 'expr')
    def params(self, p): return [p[0]]

    @_('empty')
    def params(self, p): return []
    @_('empty')
    def args(self, p): return []

    @_('expr "+" expr', 'expr "-" expr', 'expr "*" expr', 'expr "/" expr',
       'expr EQ expr', 'expr NE expr', 'expr "<" expr', 'expr ">" expr',
       'expr LE expr', 'expr GE expr')
    def expr(self, p):
        return ('BINOP', p[1], p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('UNARY', '-', p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('IDENT')
    def expr(self, p):
        return ('VAR', p.IDENT)

    @_('INT', 'FLOAT')
    def expr(self, p):
        return ('NUMBER', p[0])

    @_('')
    def empty(self, p):
        pass

    def error(self, p):
        if p:
            print(f"Błąd składniowy przy tokenie {p.type} ('{p.value}') w linii {p.lineno}")
        else:
            print("Błąd składniowy: nieoczekiwany koniec pliku")

if __name__ == '__main__':
    lexer = PVGLexer()
    parser = PVGParser()
    
    text = '''
    canvas(800, 600);
    let x = 10;
    def moja_funkcja(a, b) {
        circle(a, b, 50);
    }
    for (let i = 0; i < 10; i = i + 1) {
        moja_funkcja(i * 10, 100);
    }
    '''
    result = parser.parse(lexer.tokenize(text))
    import pprint
    pprint.pprint(result)