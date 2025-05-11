from ezLexer.token import Token


__all__ = [
    "AST", "Statement", "Expression", "Program","Assignable",
    "ExprStatement",
    "IntExpr", "FloatExpr", "StringExpr", "IdExpr", "AssignExpr",
]


class AST():
    def __init__(self, token: Token = None) -> None:
        self.token: Token = token
    
    @property
    def literal(self) -> str:
        if not self.token:
            return '<None>'
        return self.token.lexeme.literal


class Assignable():...


class Statement(AST):...


class Expression(AST):...


class Program(AST):
    def __init__(self, token: Token = None) -> None:
        super().__init__(token)
        self.statemets: list[Statement] = []
    
    @property
    def literal(self) -> str:
        if self.statemets:
            return '<None>'
        return self.statemets[0].literal


class ExprStatement(Statement):
    def __init__(
            self,
            token: Token = None,
            expr: Expression = None
        ) -> None:
        super().__init__(token)
        self.expr = expr


class IntExpr(Expression):
    def __init__(
            self,
            token: Token = None,
            value: int = 0
        ) -> None:
        super().__init__(token)
        self.value: int = value


class FloatExpr(Expression):
    def __init__(
            self,
            token: Token = None,
            value: float = 0.
        ) -> None:
        super().__init__(token)
        self.value: float = value


class StringExpr(Expression):
    def __init__(
            self,
            token: Token = None,
            value: str = ''
        ) -> None:
        super().__init__(token)
        self.value: str = value


class IdExpr(Expression, Assignable):
    def __init__(
            self,
            token: Token = None,
            name: str = ''
        ) -> None:
        super().__init__(token)
        self.name: int = name


class AssignExpr(Expression):
    def __init__(
            self,
            token: Token = None,
            left: Expression = None,
            right: Expression = None
        ) -> None:
        super().__init__(token)
        self.left = left
        self.right = right
