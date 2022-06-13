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
        self.registerPrefix(token.BANG,     self.parsePrefixExpression)
        self.registerPrefix(token.MINUS,    self.parsePrefixExpression)
        self.registerPrefix(token.TRUE,     self.parseBoolean)
        self.registerPrefix(token.FALSE,    self.parseBoolean)
        self.registerPrefix(token.LPAREN,   self.parseGroupedExpression)
        self.registerPrefix(token.IF,       self.parseIfExpression)
        self.registerPrefix(token.FUNCTION, self.parseFunctionLiteral)

        self.registerInfix(token.PLUS,      self.parseInfixExpression) 
        self.registerInfix(token.MINUS,     self.parseInfixExpression) 
        self.registerInfix(token.SLASH,     self.parseInfixExpression) 
        self.registerInfix(token.ASTERISK,  self.parseInfixExpression) 
        self.registerInfix(token.EQ,        self.parseInfixExpression) 
        self.registerInfix(token.NOT_EQ,    self.parseInfixExpression) 
        self.registerInfix(token.LT,        self.parseInfixExpression) 
        self.registerInfix(token.GT,        self.parseInfixExpression)
        self.registerInfix(token.LPAREN,    self.parseCallExpression)

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
            else:
                return program
            
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
        
        self.nextToken()
        stmt.value = self.parseExpression(LOWEST)

        if self.peekTokenIs(token.SEMICOLON):
            self.nextToken()
        
        return stmt
    
    def parseReturnStatement(self):
        stmt = ast.ReturnStatement(self.curToken, None)

        self.nextToken()
        
        stmt.value = self.parseExpression(LOWEST)

        if self.peekTokenIs(token.SEMICOLON):
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
            self.noPrefixParseFnError(self.curToken.type)
            return None
         
        leftExp = prefix()

        while not self.peekTokenIs(token.SEMICOLON) and priority < self.peekPrecedence():
            infix = None 
            if self.peekToken.type in self.infixParseFns:
                infix = self.infixParseFns[self.peekToken.type]     

            if infix is None:
                return leftExp
            
            self.nextToken()

            leftExp = infix(leftExp)
    
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

    def noPrefixParseFnError(self, token):
        msg = "no prefix parse function for {} found".format(token)
        self.errors.append(msg)
    
    def parsePrefixExpression(self):
        expression = ast.PrefixExpression(self.curToken, self.curToken.literal, None)
        self.nextToken()
        expression.right = self.parseExpression(PREFIX)
        return expression

    def peekPrecedence(self):
        if self.peekToken.type in precedences:
            return precedences[self.peekToken.type]    
        return LOWEST

    def curPrecedence(self):
        if self.curToken.type in precedences:
            return precedences[self.curToken.type]    
        return LOWEST
    
    def parseInfixExpression(self, left):
        expression = ast.InfixExpression(self.curToken, left, self.curToken.literal, None)
        precedence = self.curPrecedence()
        self.nextToken()
        expression.right = self.parseExpression(precedence)

        return expression

    def parseBoolean(self):
        return ast.Boolean(self.curToken, self.curTokenIs(token.TRUE))
    
    def parseGroupedExpression(self):
        self.nextToken()
        exp = self.parseExpression(LOWEST)

        if not self.expectPeek(token.RPAREN):
            return None
        
        return exp
    
    def parseIfExpression(self):
        expression = ast.IfExpression(self.curToken, None, None, None)

        if not self.expectPeek(token.LPAREN):
            return None
        
        self.nextToken()
        expression.condition = self.parseExpression(LOWEST)

        if not self.expectPeek(token.RPAREN):
            return None
        if not self.expectPeek(token.LBRACE):
            return None
        
        expression.consequence = self.parseBlockStatement()
    
        if self.peekTokenIs(token.ELSE):
            self.nextToken()
            if not self.expectPeek(token.LBRACE):
                return None
            expression.alternative = self.parseBlockStatement()

        return expression
    
    def parseBlockStatement(self):
        block = ast.BlockStatement(self.curToken, [])

        self.nextToken()

        while not self.curTokenIs(token.RBRACE) and not self.curTokenIs(token.EOF):
            stmt = self.parseStatement()
            if stmt is not None:
                block.statements.append(stmt)
            self.nextToken()
        
        return block
    
    def parseFunctionLiteral(self):
        lit = ast.FunctionLiteral(self.curToken, None, None)
        if not self.expectPeek(token.LPAREN):
            return None
        
        lit.parameters = self.parseFunctionParameters()
    
        if not self.expectPeek(token.LBRACE):
            return None
        
        lit.body = self.parseBlockStatement()
    
        return lit
    
    def parseFunctionParameters(self):
        identifiers = []

        if self.peekTokenIs(token.RPAREN):
            self.nextToken()
            return identifiers
        
        self.nextToken()

        ident = ast.Identifier(self.curToken, self.curToken.literal)
        identifiers.append(ident)

        while self.peekTokenIs(token.COMMA):
            self.nextToken()
            self.nextToken()
            ident = ast.Identifier(self.curToken, self.curToken.literal)
            identifiers.append(ident)
        
        if not self.expectPeek(token.RPAREN):
            return None
        
        return identifiers
    
    def parseCallExpression(self, function):
        exp = ast.CallExpression(self.curToken, function, None)
        exp.arguments = self.parseCallArguments()
        return exp
    
    def parseCallArguments(self):
        args = []

        if self.peekTokenIs(token.RPAREN):
            self.nextToken()
            return args
        
        self.nextToken()

        args.append(self.parseExpression(LOWEST))

        while self.peekTokenIs(token.COMMA):
            self.nextToken()
            self.nextToken()
            args.append(self.parseExpression(LOWEST))
        
        if not self.expectPeek(token.RPAREN):
            return None
        
        return args