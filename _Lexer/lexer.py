from curses.ascii import isalpha, isdigit
import _Token.token as token

class Lexer():
    def __init__(self, input : str):
        self.input          = input
        self.position       = 0
        self.readPosition   = 0
        self.ch             = None
        self.readChar()

    # Get current character in self.ch
    def readChar(self):
        if self.readPosition >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.readPosition]
        
        self.position = self.readPosition
        self.readPosition = self.readPosition + 1
    
    # Get next tokne
    def nextToken(self) -> token.Token:
        tok = tok = token.newToken(token.ILLEGAL, self.ch)

        self.skipWhitespace()

        if self.ch == "=":
            if self.peekChar() == "=":
                ch = self.ch
                self.readChar()
                tok = token.newToken(token.EQ, ch + self.ch)
            else:
                tok = token.newToken(token.ASSIGN, self.ch)

        elif self.ch ==  ";":
            tok = token.newToken(token.SEMICOLON, self.ch)

        elif self.ch ==  "+":
            tok = token.newToken(token.PLUS, self.ch)

        if self.ch == "-":
            tok = token.newToken(token.MINUS, self.ch)

        if self.ch == "!":
            if self.peekChar() == "=":
                ch = self.ch
                self.readChar()
                tok = token.newToken(token.NOT_EQ, ch + self.ch)
            else:
                tok = token.newToken(token.BANG, self.ch)

        if self.ch == "/":
            tok = token.newToken(token.SLASH, self.ch)

        if self.ch == "*":
            tok = token.newToken(token.ASTERISK, self.ch) 

        if self.ch == "<":
            tok = token.newToken(token.LT, self.ch) 

        if self.ch == ">":
            tok = token.newToken(token.GT, self.ch) 

        if self.ch == "-":
            tok = token.newToken(token.MINUS, self.ch)

        elif self.ch ==  "(":
            tok = token.newToken(token.LPAREN, self.ch)

        elif self.ch ==  ")":
            tok = token.newToken(token.RPAREN, self.ch)

        elif self.ch ==  "{":
            tok = token.newToken(token.LBRACE, self.ch)

        elif self.ch ==  "}":
            tok = token.newToken(token.RBRACE, self.ch)

        elif self.ch ==  ",":
            tok = token.newToken(token.COMMA, self.ch)
        
        elif self.ch == '"':
            tok = token.newToken(token.STRING, self.readString())
        
        elif self.ch == "[":
            tok = token.newToken(token.LBRACKET, self.ch)

        elif self.ch == "]":
            tok = token.newToken(token.RBRACKET, self.ch)
        
        elif self.ch == ":":
            tok = token.newToken(token.COLON, self.ch)

        elif self.ch ==  0:
            tok = token.newToken(token.EOF, "")

        else:
            if self.isLetter(self.ch):
                tok.literal = self.readToken(self.isLetter)
                tok.type    = token.lookupIdent(tok.literal)
                return tok
            if self.isDigit(self.ch):
                tok.literal = self.readToken(self.isDigit)
                tok.type = token.INT
                return tok
        
        self.readChar()
        return tok

    def isLetter(self, ch : str) -> bool:
        return isalpha(ch) or ch == '_'
    
    def isDigit(self, ch : str) -> bool:
        return isdigit(ch)
    
    # read a token until it satisfies verifyFunction (both for literals and digits)
    def readToken(self, verifyFunction : callable) -> str:
        position = self.position
        while verifyFunction(self.ch):
            self.readChar()
        
        return self.input[position : self.position]

    def skipWhitespace(self):
        while self.ch in [' ', '\t', '\n', '\r']:
            self.readChar()

    # get next character
    def peekChar(self) -> str:
        if self.readPosition >= len(self.input):
            return 0
        
        return self.input[self.readPosition]
    
    def readString(self) -> str:
        position = self.position + 1

        while True:
            self.readChar()
            if self.ch in ['"', 0]:
                break
        
        return self.input[position: self.position]