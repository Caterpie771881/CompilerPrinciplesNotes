import re
from enum import Enum
from .utils import unions
from .utils import Position


__all__ = [
    "TokenType", "Lexeme", "Token",
    "keywords", "operators", "separators",
    "lexing_rules"
]


class TokenType(Enum):
    EOF         = "EOF"
    ILLEGAL     = "ILLEGAL"
    WHITESPACE  = "WHITESPACE"
    NEWLINE     = "NEWLINE"
    IDENTIFIER  = "IDENTIFIER"
    STRING      = "STRING"
    # keyword
    KEYWORD     = "KEYWORD"
    IF          = "IF"
    ELSE        = "ELSE"
    ELIF        = "ELIF"
    TRUE        = "TRUE"
    FALSE       = "FALSE"
    FUNCTION    = "FUNCTION"
    RETURN      = "RETURN"
    NULL        = "NULL"
    CLASS       = "CLASS"
    IMPORT      = "IMPORT"
    AS          = "AS"
    AND         = "AND"
    OR          = "OR"
    NOT         = "NOT"
    # operator
    OPERATOR    = "OPERATOR"
    PLUS        = '+'
    MINUS       = '-'
    ASTERISK    = '*'
    SLASH       = '/'
    MOD         = '%'
    ASSIGN      = '='
    EQ          = '=='
    LT          = '<'
    GT          = '>'
    DOT         = '.'
    LOGIC_NOT   = '!'
    LOGIC_AND   = '&&'
    LOGIC_OR    = '||'
    NOT_EQ      = '!='
    COLON       = ':'
    BIT_AND     = '&'
    BIT_OR      = '|'
    BIT_NOT     = '~'
    BIT_XOR     = '^'
    # number
    INT         = "INT"
    FLOAT       = "FLOAT"
    # separator
    SEPARATOR   = "SEPARATOR"
    COMMA       = ','
    SEMICOLON   = ';'
    LPAREN      = '('
    RPAREN      = ')'
    LBRACKET    = '['
    RBRACKET    = ']'
    LBRACE      = '{'
    RBRACE      = '}'


keywords: dict[str, TokenType] = {
    'if':       TokenType.IF,
    'else':     TokenType.ELSE,
    'true':     TokenType.TRUE,
    'false':    TokenType.FALSE,
    'fn':       TokenType.FUNCTION,
    'return':   TokenType.RETURN,
    'null':     TokenType.NULL,
    'elif':     TokenType.ELIF,
    'class':    TokenType.CLASS,
    'import':   TokenType.IMPORT,
    'as':       TokenType.AS,
    'and':      TokenType.AND,
    'or':       TokenType.OR,
    'not':      TokenType.NOT,
}

operators: dict[str, TokenType] = {
    '+':    TokenType.PLUS,
    '-':    TokenType.MINUS,
    '*':    TokenType.ASTERISK,
    '/':    TokenType.SLASH,
    '%':    TokenType.MOD,
    '=':    TokenType.ASSIGN,
    '==':   TokenType.EQ,
    '>':    TokenType.GT,
    '<':    TokenType.LT,
    '.':    TokenType.DOT,
    '!':    TokenType.LOGIC_NOT,
    '!=':   TokenType.NOT_EQ,
    ':':    TokenType.COLON,
    '&':    TokenType.BIT_AND,
    '|':    TokenType.BIT_OR,
    '&&':   TokenType.LOGIC_AND,
    '||':   TokenType.LOGIC_OR,
    '~':    TokenType.BIT_NOT,
    '^':    TokenType.BIT_XOR,
}

separators: dict[str, TokenType] = {
    ',':    TokenType.COMMA,
    ';':    TokenType.SEMICOLON,
    '(':    TokenType.LPAREN,
    ')':    TokenType.RPAREN,
    '[':    TokenType.LBRACKET,
    ']':    TokenType.RBRACKET,
    '{':    TokenType.LBRACE,
    '}':    TokenType.RBRACE,
}

lexing_rules: dict[TokenType, re.Pattern] = {
    TokenType.KEYWORD:      re.compile(r"(" + unions(keywords) + r")\b"),
    TokenType.IDENTIFIER:   re.compile(r"[A-Za-z_][A-Za-z0-9_]*"),
    TokenType.OPERATOR:     re.compile(unions(operators)),
    TokenType.SEPARATOR:    re.compile(unions(separators)),
    TokenType.FLOAT:        re.compile(r"(([1-9]\d*)|\d)\.\d*"),
    TokenType.INT:          re.compile(r"([1-9]\d*)|\d"),
    TokenType.STRING:       re.compile(r"\".*?\"|'.*?'"),
    TokenType.NEWLINE:      re.compile(r"\n|\r|\r\n"),
    TokenType.WHITESPACE:   re.compile(r"\s+"),
    TokenType.ILLEGAL:      re.compile(r"."),
}


class Lexeme():
    def __init__(
        self,
        literal: str,
        position: Position
    ) -> None:
        self.literal: str = literal
        self.position: Position = position


class Token():
    def __init__(
            self,
            type_: TokenType,
            lexeme: Lexeme,
        ) -> None:
        self.type: TokenType = type_
        self.lexeme: Lexeme = lexeme
    
    def __str__(self) -> str:
        return f"[{self.type.name} '{self.lexeme.literal}']"

