from .lexer import Token


__all__ = ["ASTNode", "Quantifier", "SingelChar", "PrefixExpr", "InfixExpr", "SuffixExpr",
           "Concat", "Union", "Closure", "Epsilon", "Qmark", "Plus", "AnyChar"]


class ASTNode():
    def __init__(self, token: Token = None) -> None:
        self.token: Token = token

    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def __str__(self) -> str:
        return self.tokenLiteral()


class Quantifier():...


class SingelChar(ASTNode):
    def __init__(
            self,
            token: Token = None,
            value: str = '',
        ) -> None:
        self.token: Token = token
        self.value: str = value
    
    def __str__(self) -> str:
        return self.value


class AnyChar(ASTNode):
    def __str__(self) -> str:
        return "<any>"


class Epsilon(ASTNode):
    def __str__(self) -> str:
        return "<e>"


class PrefixExpr(ASTNode):
    def __init__(
            self,
            token: Token = None,
            operator: str = '',
            right: ASTNode = None
        ) -> None:
        self.token: Token = token
        self.operator: str = operator
        self.right: ASTNode = right
    
    def __str__(self) -> str:
        return f"({self.operator}{self.right})"


class InfixExpr(ASTNode):
    def __init__(
            self,
            token: Token = None,
            left: ASTNode = None,
            operator: str = '',
            right: ASTNode = None
        ) -> None:
        self.token: Token = token
        self.left: ASTNode = left
        self.operator: str = operator
        self.right: ASTNode = right
    
    def __str__(self) -> str:
        return f"({self.left}{self.operator}{self.right})"


class SuffixExpr(ASTNode):
    def __init__(
            self,
            token: Token = None,
            left: ASTNode = None,
            operator: str = '',
        ) -> None:
        self.token: Token = token
        self.left: ASTNode = left
        self.operator: str = operator
    
    def __str__(self) -> str:
        return f"({self.left}{self.operator})"


class Concat(InfixExpr):
    """It means a concat expr. such as `AB`"""


class Union(InfixExpr):
    """It means a union expr. such as `A|B`"""


class Closure(SuffixExpr, Quantifier):
    """It means a closure expr. such as `A*`"""


class Qmark(SuffixExpr, Quantifier):
    """a candy. `A?` equals to `A|ε`"""


class Plus(SuffixExpr, Quantifier):
    """a candy. `A+` equals to `A|A*`"""

