from .token import *


class Lexer():
    def __init__(self, input_: str):
        self.input = input_
        self.fpos = 0
        self.bpos = 1
    
    @property
    def current_char(self) -> str:
        if self.fpos >= len(self.input):
            return ''
        return self.input[self.fpos]
    
    @property
    def peek_char(self) -> str:
        if self.bpos >= len(self.input):
            return ''
        return self.input[self.bpos]
    
    def read_head(self) -> None:
        self.fpos += 1
        self.bpos += 1
    
    def handle_escape(self, char: str) -> Token:
        match char:
            case 'n':
                return Token(TokenType.CHAR, '\n')
            case 'r':
                return Token(TokenType.CHAR, '\r')
            case 't':
                return Token(TokenType.CHAR, '\t')
            case '\\' | '|' | '*' | '(' | ')'\
                | ' ' | '.' | '?' | '+' | '"'\
                | "'" :
                return Token(TokenType.CHAR, char)
            case '':
                raise SyntaxError("Escape character must be followed by content")
            case _:
                raise SyntaxError(f"Unsupport character {'\\' + char}")
    
    def next_token(self) -> Token:
        while self.current_char.isspace() and self.current_char != ' ':
            self.read_head()
        
        token: Token
        cc = self.current_char
        pc = self.peek_char
        match cc:
            case '':
                token = Token(TokenType.EOF, cc)
            case '|':
                token = Token(TokenType.UNION, cc)
            case '*':
                token = Token(TokenType.CLOSURE, cc)
            case '(':
                token = Token(TokenType.LBRACKET, cc)
            case ')':
                token = Token(TokenType.RBRACKET, cc)
            case '.':
                token = Token(TokenType.ANY, cc)
            case '?':
                token = Token(TokenType.QMARK, cc)
            case '+':
                token = Token(TokenType.PLUS, cc)
            case '\\':
                self.read_head()
                return self.handle_escape(pc)
            case _:
                token = Token(TokenType.CHAR, cc)

        self.read_head()
        return token
