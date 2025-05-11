from ezLexer.token import *
from ..ast import *
from typing import Callable
from enum import IntEnum
from enum import auto


type nuds = Callable[[], AST]
type leds = Callable[[AST], AST]


class ExprLevel(IntEnum):
    LOWEST      = auto()
    EQUALS      = auto() # ==
    LESSGREATER = auto() # > or <
    SUM         = auto() # +
    PRODUCT     = auto() # *
    PREFIX      = auto() # -X or !X
    CALL        = auto() # func(X)
    INDEX_VISIT = auto() # array[idx] or X.Y


token_level: dict[TokenType, ExprLevel] = {
    TokenType.EQ:       ExprLevel.EQUALS,
    TokenType.NOT_EQ:   ExprLevel.EQUALS,
    TokenType.LT:       ExprLevel.LESSGREATER,
    TokenType.GT:       ExprLevel.LESSGREATER,
    TokenType.PLUS:     ExprLevel.SUM,
    TokenType.MINUS:    ExprLevel.SUM,
    TokenType.SLASH:    ExprLevel.PRODUCT,
    TokenType.ASTERISK: ExprLevel.PRODUCT,
    TokenType.LPAREN:   ExprLevel.CALL,
    TokenType.LBRACKET: ExprLevel.INDEX_VISIT,
    TokenType.DOT:      ExprLevel.INDEX_VISIT,
}


class Parser():
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.ptr: int = 0
        self.nuds: dict[TokenType, nuds] = {}
        self.leds: dict[TokenType, leds] = {}


    def parse_program(self) -> Program:
        program: Program = Program()


    def parse_expr_statement(self) -> ExprStatement:
        ...
