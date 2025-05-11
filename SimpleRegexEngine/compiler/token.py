from enum import Enum


__all__ = ["TokenType", "Token"]


class TokenType(Enum):
    EOF             = 'EOF'
    CHAR            = 'CHAR'
    UNION           = '|'
    CLOSURE         = '*'
    LBRACKET        = '('
    RBRACKET        = ')'
    ANY             = 'ANY'
    QMARK           = '?'
    PLUS            = '+'
    # TODO: 支持懒惰模式的运算符
    LAZY_CLOSURE    = '*?'
    LAZY_QMARK      = '??'
    LAZY_PLUS       = '+?'


class Token():
    def __init__(self, type_: TokenType, literal: str):
        self.type = type_
        self.literal = literal

    def __str__(self) -> str:
        return f"Token[type={self.type.name}, literal='{self.literal}']"
