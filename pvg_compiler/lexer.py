# pvg_compiler/lexer.py
from sly import Lexer

class PVGLexer(Lexer):
    def __init__(self):
        super().__init__()
        self.has_error = False
        self.source_code = ""

    tokens = {
        IDENT, INT, FLOAT, STRING,
        CANVAS, BACKGROUND, FILL, STROKE, STROKE_WIDTH, OPACITY, FONT_SIZE, FONT_FAMILY,
        CIRCLE, RECT, LINE, ELLIPSE, POLYGON, POLYLINE, TEXT_CMD, PATH,
        ROTATE, TRANSLATE, SCALE,
        DEF, FOR, WHILE, LET, IF, ELSE, PRINT, BREAK, CONTINUE,
        SIN, COS, TAN, SQRT, LOG, EXP, ABS, ROUND, CEIL, FLOOR,
        EQ, LE, GE, NE, AND, OR, NOT
    }

    ignore = ' \t'
    literals = { '+', '-', '*', '/', '%', '=', '(', ')', '{', '}', ';', ',', '<', '>', '[', ']' }

    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    # Słowa kluczowe
    IDENT['canvas']         = CANVAS
    IDENT['background']     = BACKGROUND
    IDENT['fill']           = FILL
    IDENT['color']          = FILL
    IDENT['stroke']         = STROKE
    IDENT['stroke_width']   = STROKE_WIDTH
    IDENT['opacity']        = OPACITY
    IDENT['font_size']      = FONT_SIZE
    IDENT['font_family']    = FONT_FAMILY
    
    IDENT['circle']         = CIRCLE
    IDENT['rect']           = RECT
    IDENT['line']           = LINE
    IDENT['ellipse']        = ELLIPSE
    IDENT['polygon']        = POLYGON
    IDENT['polyline']       = POLYLINE
    IDENT['text']           = TEXT_CMD
    IDENT['path']           = PATH
    
    IDENT['rotate']         = ROTATE
    IDENT['translate']      = TRANSLATE
    IDENT['scale']          = SCALE
    
    IDENT['def']            = DEF
    IDENT['for']            = FOR
    IDENT['while']          = WHILE
    IDENT['let']            = LET
    IDENT['if']             = IF
    IDENT['else']           = ELSE
    IDENT['print']          = PRINT
    IDENT['break']          = BREAK
    IDENT['continue']       = CONTINUE
    
    IDENT['sin']            = SIN
    IDENT['cos']            = COS
    IDENT['tan']            = TAN
    IDENT['sqrt']           = SQRT
    IDENT['log']            = LOG
    IDENT['exp']            = EXP
    IDENT['abs']            = ABS
    IDENT['round']          = ROUND
    IDENT['ceil']           = CEIL
    IDENT['floor']          = FLOOR
    
    IDENT['and']            = AND
    IDENT['or']             = OR
    IDENT['not']            = NOT

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
        self.has_error = True
        print(f"🔍 Błąd Leksykalny w linii {self.lineno}: Nierozpoznany znak '{t.value[0]}'")
        self.index += 1