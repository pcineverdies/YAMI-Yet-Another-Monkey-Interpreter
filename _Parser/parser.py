from ast import Expression
import _Ast.ast as ast
import _Lexer.lexer as lexer
import _Token.token as token
from _Parser.priority import *

class Parser:
    def __init__(self, lexer):
        self.l              = lexer
        self.curToken       = None
        self.peekToken      = None
        self.errors         = []
        self.prefixParseFns = {}
        self.infixParseFns  = {}

        self.registerPrefix(token.IDENT,    self.parseIdentifier)
        self.registerPrefix(token.INT,      self.parseIntegerLiteral)

        self.nextToken()
        self.nextToken()

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.l.nextToken()
    
    def parseProgram(self):
        program = ast.Program()

        while not self.curTokenIs(token.EOF):
            stmt = self.parseStatement()

            if stmt != None:
                program.statements.append(stmt)
            
            self.nextToken()
        
        return program
    
    def parseStatement(self):
        if self.curToken.type == token.LET:
            return self.parseLetStatement()
        elif self.curToken.type == token.RETURN:
            return self.parseReturnStatement()
        else:
            return self.parseExpressionStatement()
    
    def parseLetStatement(self):
        stmt = ast.LetStatement(self.curToken, None, None)

        if not self.expectPeek(token.IDENT):
            return None
        
        stmt.name = ast.Identifier(self.curToken, self.curToken.literal)

        if not self.expectPeek(token.ASSIGN):
            return None 
        
        while not self.curTokenIs(token.SEMICOLON):
            self.nextToken()
        
        return stmt
    
    def parseReturnStatement(self):
        stmt = ast.ReturnStatement(self.curToken, None)

        self.nextToken()

        while not self.curTokenIs(token.SEMICOLON):
            self.nextToken()
        
        return stmt

    def curTokenIs(self, t):
        return self.curToken.type == t

    def peekTokenIs(self, t):
        return self.peekToken.type == t

    def expectPeek(self, t):
        if self.peekTokenIs(t):
            self.nextToken()
            return True
        
        self.peekError(t)
        return False
    
    def getErrors(self):
        return self.errors
    
    def peekError(self, token):
        msg = "expected next token to be {}, got {}".format(token, self.peekToken.type)
        self.errors.append(msg)

    def registerPrefix(self, tokenType, fn):
        self.prefixParseFns[tokenType] = fn
    
    def registerInfix(self, tokenType, fn):
        self.infixParseFns[tokenType] = fn

    def parseExpressionStatement(self):
        stmt = ast.ExpressionStatement(self.curToken, None)
        stmt.expression = self.parseExpression(LOWEST)

        if self.peekTokenIs(token.SEMICOLON):
            self.nextToken()
        
        return stmt

    def parseExpression(self, priority):
        prefix = None

        if self.curToken.type in self.prefixParseFns:
            prefix = self.prefixParseFns[self.curToken.type]

        if prefix is None:
            return None
        
        leftExp = prefix()
    
        return leftExp

    def parseIdentifier(self):
        return ast.Identifier(self.curToken, self.curToken.literal)

    def parseIntegerLiteral(self):
        lit = ast.IntegerLiteral(self.curToken, None)

        try:
            lit.value = int(self.curToken.literal)
        except ValueError:
            msg = "could not parse {} as integer".format(self.curToken.literal)
            self.errors.append(msg)
            return None

        return lit