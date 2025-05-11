from .token import *
import re
from .utils import Position
from copy import copy


class Lexer():
    def __init__(self, input_: str):
        self.input: str = input_
        self.ptr: int = 0
        self.cur_pos: Position = Position(1, 1)
        self._token_stream: list[Token] = []


    def raise_error(self, msg: str) -> None:
        raise Exception(
            f"line: {self.cur_pos.line} column: {self.cur_pos.column}\n\t'{msg}")


    def match_rules(self, code: str) -> tuple[TokenType, re.Match[str]]:
        for token_type, pattern in lexing_rules.items():
            m = pattern.match(code)
            if not m:
                continue
            return token_type, m
        self.raise_error("Can not find any TokenType to match current code")


    def next_token(self) -> Token:
        lexeme: Lexeme = Lexeme(
            literal='',
            position=copy(self.cur_pos),
        )
        token: Token = Token(TokenType.EOF, lexeme)
        if self.ptr >= len(self.input):
            return token
        
        cur_code = self.input[self.ptr:]
        token_type, match = self.match_rules(cur_code)
        lexeme.literal = match.group()

        match token_type:
            case TokenType.KEYWORD:
                keyword_type = keywords.get(lexeme.literal)
                if not keyword_type:
                    self.raise_error(f"'{lexeme.literal}' is not keyword")
                token = Token(keyword_type, lexeme)
            case TokenType.OPERATOR:
                operator_type = operators.get(lexeme.literal)
                if not operator_type:
                    self.raise_error(f"'{lexeme.literal}' is not operator")
                token = Token(operator_type, lexeme)
            case TokenType.SEPARATOR:
                separator_type = separators.get(lexeme.literal)
                if not separator_type:
                    self.raise_error(f"'{lexeme.literal}' is not separator")
                token = Token(separator_type, lexeme)
            case TokenType.NEWLINE:
                self.cur_pos.line += 1
                self.cur_pos.column = 0
                token = Token(TokenType.NEWLINE, lexeme)
            case TokenType.STRING:
                lexeme.literal = lexeme.literal[1:-1]
                token = Token(TokenType.STRING, lexeme)
            case _:
                token = Token(token_type, lexeme)
        
        self.ptr += match.end()
        self.cur_pos.column += match.end()
        return token

    @property
    def token_stream(self) -> list[Token]:
        if self._token_stream:
            return self._token_stream
        while True:
            token = self.next_token()
            match token.type:
                case TokenType.EOF:
                    break
                case TokenType.WHITESPACE | TokenType.NEWLINE:
                    continue
                case _:
                    self._token_stream.append(token)
        return self._token_stream
