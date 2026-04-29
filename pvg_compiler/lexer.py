# pvg_compiler/lexer.py
from sly import Lexer

class PVGLexer(Lexer):
    tokens = {
        IDENT, INT, FLOAT, STRING,
        CANVAS, BACKGROUND, COLOR, STROKE_WIDTH, OPACITY,
        CIRCLE, RECT, LINE, ELLIPSE, POLYGON,
        DEF, FOR, WHILE, LET, IF, ELSE, PRINT,
        SIN, COS, SQRT,
        EQ, LE, GE, NE, AND, OR
    }

    ignore = ' \t'
    literals = { '+', '-', '*', '/', '=', '(', ')', '{', '}', ';', ',', '<', '>' }

    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENT['canvas']         = CANVAS
    IDENT['background']     = BACKGROUND
    IDENT['color']          = COLOR
    IDENT['stroke_width']   = STROKE_WIDTH
    IDENT['opacity']        = OPACITY
    IDENT['circle']         = CIRCLE
    IDENT['rect']           = RECT
    IDENT['line']           = LINE
    IDENT['ellipse']        = ELLIPSE
    IDENT['polygon']        = POLYGON
    IDENT['def']            = DEF
    IDENT['for']            = FOR
    IDENT['while']          = WHILE
    IDENT['let']            = LET
    IDENT['if']             = IF
    IDENT['else']           = ELSE
    IDENT['print']          = PRINT
    IDENT['sin']            = SIN
    IDENT['cos']            = COS
    IDENT['sqrt']           = SQRT
    IDENT['and']            = AND
    IDENT['or']             = OR

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