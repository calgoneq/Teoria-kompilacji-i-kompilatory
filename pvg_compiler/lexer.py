from sly import Lexer

class PVGLexer(Lexer):
    tokens = {
        IDENT, INT, FLOAT, STRING,
        CANVAS, BACKGROUND, COLOR, CIRCLE, RECT, LINE,
        DEF, FOR, WHILE, LET, IF, ELSE,
        EQ, LE, GE, NE
    }

    ignore = ' \t'
    literals = { '+', '-', '*', '/', '=', '(', ')', '{', '}', ';', ',', '<', '>' }

    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENT['canvas']     = CANVAS
    IDENT['background'] = BACKGROUND
    IDENT['color']      = COLOR
    IDENT['circle']     = CIRCLE
    IDENT['rect']       = RECT
    IDENT['line']       = LINE
    IDENT['def']        = DEF
    IDENT['for']        = FOR
    IDENT['while']      = WHILE
    IDENT['let']        = LET
    IDENT['if']         = IF
    IDENT['else']       = ELSE

    EQ = r'=='
    LE = r'<='
    GE = r'>='
    NE = r'!='
    
    STRING = r'\"(.*?)\"'
    FLOAT  = r'\d+\.\d+'
    INT    = r'\d+'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\#.*')
    def ignore_comment(self, t):
        pass

    def error(self, t):
        print(f"Linia {self.lineno}: Nieoczekiwany znak '{t.value[0]}'")
        self.index += 1

if __name__ == '__main__':
    data = 'canvas(800, 600); # Komentarz \n color("#ff0000");'
    lexer = PVGLexer()
    for tok in lexer.tokenize(data):
        print(tok)