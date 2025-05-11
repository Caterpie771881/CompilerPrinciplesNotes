from .lexer import Lexer
from .parser import Parser
from .ast import *
from ..fa import *


__all__ = ["Lexer", "Parser", "NFABuilder", "compile"]


# TODO: 添加缓存
_cache = {}


class NFABuilder():
    def __init__(self, ast: ASTNode):
        self.ast: ASTNode = ast
    
    def ast2nfa(self, node: ASTNode) -> NFA:
        match node:
            case SingelChar():
                return NFA.singlechar(node.value)
            case Epsilon():
                return NFA.epsilon()
            case Concat():
                left = self.ast2nfa(node.left)
                right = self.ast2nfa(node.right)
                return left.concat(right)
            case Union():
                left = self.ast2nfa(node.left)
                right = self.ast2nfa(node.right)
                return left.union(right)
            case Closure():
                left = self.ast2nfa(node.left)
                return left.closure()
            case Qmark():
                left = self.ast2nfa(node.left)
                return left.union(NFA.epsilon())
            case Plus():
                left = self.ast2nfa(node.left)
                right = self.ast2nfa(node.left).closure()
                return left.concat(right)
            case AnyChar():
                return NFA.anychar()
            case _:
                raise TypeError(f"Unsupport ASTNode {node}")

    def build(self) -> NFA:
        return self.ast2nfa(self.ast)


def compile(regex: str) -> DFA:
    ast = Parser(Lexer(regex)).parse_expr()
    nfa = NFABuilder(ast).build()
    dfa = subset_construction(nfa)
    min_dfa = hopcroft(dfa)
    return min_dfa
