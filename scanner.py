from tokens import Token, Token_type
from typing import Any
from lox import *

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.__keywords = create_keyword_dict()

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(Token_type.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def scan_token(self):
        c: str = self.advance()
        match c:
            case '(': self.add_token(Token_type.LEFT_PAREN)
            case ')': self.add_token(Token_type.RIGHT_PAREN)
            case '{': self.add_token(Token_type.LEFT_BRACE)
            case '}': self.add_token(Token_type.RIGHT_BRACE)
            case ',': self.add_token(Token_type.COMMA)
            case '.': self.add_token(Token_type.DOT)
            case '-': self.add_token(Token_type.MINUS)
            case '+': self.add_token(Token_type.PLUS)
            case ';': self.add_token(Token_type.SEMICOLON)
            case '*': self.add_token(Token_type.STAR)

            case '!': self.add_token(Token_type.BANG_EQUAL if self.check() else Token_type.BANG)
            case '=': self.add_token(Token_type.EQUAL_EQUAL if self.check() else Token_type.EQUAL)
            case '<': self.add_token(Token_type.LESS_EQUAL if self.check() else Token_type.LESS)
            case '>': self.add_token(Token_type.GREATER_EQUAL if self.check() else Token_type.GREATER)

            case '/':
                if self.check(expected='/'):
                    while self.peek() != '\n' and not self.is_at_end(): self.advance()
                elif self.check(expected='*'):
                    while self.peek() != '*' and self.peek_next() != '/' and not self.is_at_end():
                        if self.peek() == '\n': self.line += 1
                        self.advance()
                    self.advance()
                    self.advance()
                else:
                    self.add_token(Token_type.SLASH)

            case ' ': pass
            case '\r': pass
            case '\t': pass
            case '\n': self.line += 1

            case '"': self.string()

            case _: 
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    Lox.error(self.line, "Unexpected character")

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def add_token(self, type: Token_type, literal: Any=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def check(self, expected: str='=') -> bool:
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.is_at_end():
            Lox.error(self.line, "Unterminated string")
            return

        # the closing "
        self.advance()

        # trim the surrounding quotes
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(Token_type.STRING, value)

    def is_digit(self, c: str) -> bool:
        return '0' <= c <= '9'

    def is_alpha(self, c: str) -> bool:
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    def is_alpha_numeric(self, c: str):
        return self.is_digit(c) or self.is_alpha(c)

    def number(self):
        while self.is_digit(self.peek()): self.advance()

        # look for fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # consume the .
            self.advance()

            while self.is_digit(self.peek()): self.advance()

        self.add_token(Token_type.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self):
        while self.is_alpha_numeric(self.peek()): self.advance()

        text = self.source[self.start : self.current]
        type = self.__keywords.get(text)
        if type == None: type = Token_type.IDENTIFIER
        self.add_token(type)
        
def create_keyword_dict():
    dict = {}
    dict["and"] = Token_type.AND
    dict["class"] = Token_type.CLASS
    dict["else"] = Token_type.ELSE
    dict["false"] = Token_type.FALSE
    dict["for"] = Token_type.FOR
    dict["fun"] = Token_type.FUN
    dict["if"] = Token_type.IF
    dict["nil"] = Token_type.NIL
    dict["or"] = Token_type.OR
    dict["print"] = Token_type.PRINT
    dict["return"] = Token_type.RETURN
    dict["super"] = Token_type.SUPER
    dict["this"] = Token_type.THIS
    dict["true"] = Token_type.TRUE
    dict["var"] = Token_type.VAR
    dict["while"] = Token_type.WHILE

    return dict
