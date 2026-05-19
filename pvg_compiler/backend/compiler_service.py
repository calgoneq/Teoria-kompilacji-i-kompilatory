
import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lexer import PVGLexer
from parser import PVGParser
from generator import SVGGenerator, SemanticError

class CompilerService:
    
    @staticmethod
    def _ast_to_dict(node):
        
        if node is None:
            return None
        if isinstance(node, (int, float)):
            return {"type": "LITERAL", "value": str(node), "kind": "number"}
        if isinstance(node, str):
            return {"type": "LITERAL", "value": node, "kind": "string"}
        if isinstance(node, bool):
            return {"type": "LITERAL", "value": str(node), "kind": "boolean"}
        if isinstance(node, list):
            return [CompilerService._ast_to_dict(item) for item in node]
        if isinstance(node, tuple):
            node_type = str(node[0])
            children = []
            for child in node[1:]:
                converted = CompilerService._ast_to_dict(child)
                if converted is not None:
                    children.append(converted)
            return {
                "type": node_type,
                "children": children
            }
        return {"type": "LITERAL", "value": str(node), "kind": "unknown"}

    @staticmethod
    def _classify_token(tok_type: str) -> str:
        
        keywords = {
            'CANVAS', 'BACKGROUND', 'FILL', 'STROKE', 'STROKE_WIDTH', 'OPACITY',
            'FONT_SIZE', 'FONT_FAMILY', 'CIRCLE', 'RECT', 'LINE', 'ELLIPSE',
            'POLYGON', 'POLYLINE', 'TEXT_CMD', 'PATH', 'ROTATE', 'TRANSLATE',
            'SCALE', 'DEF', 'FOR', 'WHILE', 'LET', 'IF', 'ELSE', 'PRINT',
            'BREAK', 'CONTINUE'
        }
        math_funcs = {'SIN', 'COS', 'TAN', 'SQRT', 'LOG', 'EXP', 'ABS', 'ROUND', 'CEIL', 'FLOOR'}
        operators = {'EQ', 'NE', 'LE', 'GE', 'AND', 'OR', 'NOT'}
        numbers = {'INT', 'FLOAT'}

        if tok_type in keywords:
            return 'keyword'
        if tok_type in math_funcs:
            return 'function'
        if tok_type in operators:
            return 'operator'
        if tok_type in numbers:
            return 'number'
        if tok_type == 'STRING':
            return 'string'
        if tok_type == 'IDENT':
            return 'identifier'
        return 'punctuation'

    def tokenize(self, code: str) -> dict:
        
        errors = []
        tokens = []

        capture = io.StringIO()
        try:
            with redirect_stdout(capture), redirect_stderr(capture):
                lexer = PVGLexer()
                lexer.source_code = code
                for tok in lexer.tokenize(code):
                    tokens.append({
                        "type": tok.type,
                        "value": tok.value,
                        "lineno": tok.lineno,
                        "category": self._classify_token(tok.type)
                    })

                if lexer.has_error:
                    errors.append({"message": "Wykryto błędy leksykalne", "type": "lexer"})
        except Exception as e:
            errors.append({"message": str(e), "type": "lexer"})

        captured = capture.getvalue().strip()
        if captured:
            for line in captured.split('\n'):
                if line.strip():
                    errors.append({"message": line.strip(), "type": "lexer"})

        return {
            "success": len(errors) == 0,
            "tokens": tokens,
            "errors": errors
        }

    def parse(self, code: str) -> dict:
        
        errors = []

        capture = io.StringIO()
        try:
            with redirect_stdout(capture), redirect_stderr(capture):
                lexer = PVGLexer()
                lexer.source_code = code
                tokens = list(lexer.tokenize(code))

                if lexer.has_error:
                    errors.append({"message": "Błędy leksykalne uniemożliwiają parsowanie", "type": "lexer"})
                    return {"success": False, "ast": None, "errors": errors}

                parser = PVGParser()
                parser.source_code = code
                ast = parser.parse(iter(tokens))

                if parser.has_error or not ast:
                    errors.append({"message": "Błędy składniowe", "type": "parser"})
                    captured = capture.getvalue().strip()
                    if captured:
                        for line in captured.split('\n'):
                            if line.strip():
                                errors.append({"message": line.strip(), "type": "parser"})
                    return {"success": False, "ast": None, "errors": errors}

                ast_dict = self._ast_to_dict(ast)
                return {"success": True, "ast": ast_dict, "errors": []}

        except Exception as e:
            errors.append({"message": str(e), "type": "parser"})
            return {"success": False, "ast": None, "errors": errors}

    def compile(self, code: str, include_ast: bool = False, include_tokens: bool = False) -> dict:
        
        errors = []
        svg = None
        ast_dict = None
        tokens_list = None
        output_lines = []

        if include_tokens:
            tok_result = self.tokenize(code)
            tokens_list = tok_result["tokens"]

        capture = io.StringIO()
        try:
            with redirect_stdout(capture), redirect_stderr(capture):

                lexer = PVGLexer()
                lexer.source_code = code
                tokens = list(lexer.tokenize(code))

                if lexer.has_error:
                    errors.append({"message": "Błędy leksykalne", "type": "lexer"})
                    captured = capture.getvalue().strip()
                    if captured:
                        output_lines.append(captured)
                    return {
                        "success": False, "svg": None, "ast": None,
                        "tokens": tokens_list, "errors": errors,
                        "output": "\n".join(output_lines)
                    }

                parser = PVGParser()
                parser.source_code = code
                ast = parser.parse(iter(tokens))

                if parser.has_error or not ast:
                    errors.append({"message": "Błędy składniowe", "type": "parser"})
                    captured = capture.getvalue().strip()
                    if captured:
                        output_lines.append(captured)
                    return {
                        "success": False, "svg": None, "ast": None,
                        "tokens": tokens_list, "errors": errors,
                        "output": "\n".join(output_lines)
                    }

                if include_ast:
                    ast_dict = self._ast_to_dict(ast)

                generator = SVGGenerator()
                svg = generator.generate(ast)

        except SemanticError as e:
            errors.append({"message": f"Błąd semantyczny: {str(e)}", "type": "semantic"})
        except Exception as e:
            errors.append({"message": f"Nieoczekiwany błąd: {str(e)}", "type": "runtime"})

        captured = capture.getvalue().strip()
        if captured:
            output_lines.append(captured)

        return {
            "success": len(errors) == 0 and svg is not None,
            "svg": svg,
            "ast": ast_dict,
            "tokens": tokens_list,
            "errors": errors,
            "output": "\n".join(output_lines)
        }
