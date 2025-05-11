from typing import Callable
from .ast import *
from .token import *
from .lexer import Lexer


OPERATOR_LEVELS: dict[TokenType, int] = {
    TokenType.CLOSURE:  40,
    TokenType.QMARK:    40,
    TokenType.PLUS:     40,
    TokenType.LBRACKET: 30,
    TokenType.CHAR:     20,
    TokenType.ANY:      20,
    TokenType.UNION:    10,
}


def get_token_level(token: Token) -> int:
    return OPERATOR_LEVELS.get(token.type, 0)


class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.current_token: Token = Token(TokenType.EOF, '')
        self.peek_token: Token = Token(TokenType.EOF, '')
        self.nuds: dict[TokenType, Callable[[], ASTNode]] = {
            TokenType.CHAR:     self.parse_singelchar,
            TokenType.LBRACKET: self.parse_group,
            TokenType.ANY:      self.parse_anychar,
        }
        self.leds: dict[TokenType, Callable[[ASTNode], ASTNode]] = {
            TokenType.CHAR:     self.parse_concat,
            TokenType.LBRACKET: self.parse_concat,
            TokenType.UNION:    self.parse_union,
            TokenType.CLOSURE:  self.parse_closure,
            TokenType.QMARK:    self.parse_qmark_candy,
            TokenType.PLUS:     self.parse_plus_candy,
            TokenType.ANY:      self.parse_concat,
        }
        self.next_token()
        self.next_token()

    def next_token(self) -> None:
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()
    
    def expect_peek(self, token_type: TokenType) -> None:
        peek_type = self.peek_token.type
        if peek_type != token_type:
            raise SyntaxError(
                f"Unexpect token: want {token_type.name}, got {peek_type.name}")
        self.next_token()
    
    @property
    def current_level(self) -> int:
        return get_token_level(self.current_token)
    
    @property
    def peek_level(self) -> int:
        return get_token_level(self.peek_token)
    
    def parse_expr(self, level: int = 0) -> ASTNode:
        nuds = self.nuds.get(self.current_token.type)
        if not nuds:
            raise TypeError(f"{self.current_token.type.name} has no nuds")
        leftExpr = nuds()

        while (
            self.peek_token.type != TokenType.EOF
            and level < self.peek_level
        ):
            leds = self.leds.get(self.peek_token.type)
            if not leds:
                raise TypeError(f"{self.peek_token.type.name} has no leds")
            self.next_token()
            leftExpr = leds(leftExpr)
        
        return leftExpr
    
    def parse_singelchar(self) -> ASTNode:
        return SingelChar(self.current_token, self.current_token.literal)
    
    def parse_concat(self, left: ASTNode) -> ASTNode:
        return Concat(
            token=self.current_token,
            left=left,
            operator='~',
            right=self.parse_expr(self.current_level)
        )
    
    def parse_group(self) -> ASTNode:
        self.next_token()
        expr = self.parse_expr()
        self.expect_peek(TokenType.RBRACKET)
        return expr

    def parse_union(self, left: ASTNode) -> ASTNode:
        token = self.current_token
        level = self.current_level
        self.next_token()
        return Union(
            token=token,
            left=left,
            operator=token.literal,
            right=self.parse_expr(level)
        )

    def parse_closure(self, left: ASTNode) -> ASTNode:
        if isinstance(left, Quantifier):
            raise SyntaxError(f"closure can not follow {left} Expr")
        return Closure(
            token=self.current_token,
            left=left,
            operator=self.current_token.literal
        )
    
    def parse_qmark_candy(self, left: ASTNode) -> ASTNode:
        if isinstance(left, Quantifier):
            raise SyntaxError(f"qmark can not follow {left} Expr")
        return Qmark(
            token=self.current_token,
            left=left,
            operator=self.current_token.literal
        )

    def parse_plus_candy(self, left: ASTNode) -> ASTNode:
        if isinstance(left, Quantifier):
            raise SyntaxError(f"plus can not follow {left} Expr")
        return Plus(
            token=self.current_token,
            left=left,
            operator=self.current_token.literal
        )
    
    def parse_anychar(self) -> ASTNode:
        return AnyChar(self.current_token)
