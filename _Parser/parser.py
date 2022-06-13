from typing import List
import _Ast.ast as ast
import _Lexer.lexer as lexer
import _Token.token as token
from _Parser.priority import *

class Parser:
    def __init__(self, lexer : lexer.Lexer):
        self.l              = lexer
        self.curToken       = None
        self.peekToken      = None
        self.errors         = []
        self.prefixParseFns = {}
        self.infixParseFns  = {}

        # prefix token functions
        self.registerPrefix(token.IDENT,    self.parseIdentifier)           # identifier
        self.registerPrefix(token.INT,      self.parseIntegerLiteral)       # int
        self.registerPrefix(token.BANG,     self.parsePrefixExpression)     # !
        self.registerPrefix(token.MINUS,    self.parsePrefixExpression)     # -
        self.registerPrefix(token.TRUE,     self.parseBoolean)              # true
        self.registerPrefix(token.FALSE,    self.parseBoolean)              # false
        self.registerPrefix(token.LPAREN,   self.parseGroupedExpression)    # ( -> grouped
        self.registerPrefix(token.IF,       self.parseIfExpression)         # if
        self.registerPrefix(token.FUNCTION, self.parseFunctionLiteral)      # fn
        self.registerPrefix(token.STRING,   self.parseStringLiteral)        # string
        self.registerPrefix(token.LBRACKET, self.parseArrayLiteral)         # [ prefix
        self.registerPrefix(token.LBRACE,   self.parseHashLiteral)          # { prefix
        
        # infix token functions
        self.registerInfix(token.PLUS,      self.parseInfixExpression)      # +
        self.registerInfix(token.MINUS,     self.parseInfixExpression)      # -
        self.registerInfix(token.SLASH,     self.parseInfixExpression)      # /
        self.registerInfix(token.ASTERISK,  self.parseInfixExpression)      # *
        self.registerInfix(token.EQ,        self.parseInfixExpression)      # =
        self.registerInfix(token.NOT_EQ,    self.parseInfixExpression)      # !=
        self.registerInfix(token.LT,        self.parseInfixExpression)      # <
        self.registerInfix(token.GT,        self.parseInfixExpression)      # >
        self.registerInfix(token.LPAREN,    self.parseCallExpression)       # ( -> call
        self.registerInfix(token.LBRACKET,  self.parseIndexExpression)      # [ -> index

        # set the value of both curToken and peekToken
        self.nextToken()
        self.nextToken()

    # get nextToken
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.l.nextToken()
    
    # start parsing
    def parseProgram(self) -> ast.Program:
        program = ast.Program()

        while not self.curTokenIs(token.EOF):
            # parse a statement, add to program.statements if it's not None
            # otherwise, end parsing operation
            stmt = self.parseStatement()

            if stmt != None:
                program.statements.append(stmt)
            else:
                return program
            self.nextToken()
    
        return program
    
    # parse the three different kind of statements : let, return, expression
    def parseStatement(self) -> ast.Statement:
        if self.curToken.type == token.LET:
            return self.parseLetStatement()
        elif self.curToken.type == token.RETURN:
            return self.parseReturnStatement()
        else:
            return self.parseExpressionStatement()
    
    # parse let statement
    def parseLetStatement(self) -> ast.LetStatement:
        stmt = ast.LetStatement(self.curToken)

        # if peek token is not an identifier, return None
        if not self.expectPeek(token.IDENT):
            return None
        
        # get the identifier
        stmt.name = ast.Identifier(self.curToken, self.curToken.literal)

        # if peek token is not an assing, return None
        if not self.expectPeek(token.ASSIGN):
            return None 
        
        self.nextToken()
        # parse following expression
        stmt.value = self.parseExpression(LOWEST)

        if self.peekTokenIs(token.SEMICOLON):
            self.nextToken()
        
        return stmt
    
    # parse return statement
    def parseReturnStatement(self) -> ast.ReturnStatement:
        stmt = ast.ReturnStatement(self.curToken)

        self.nextToken()
        # parse following expression
        stmt.value = self.parseExpression(LOWEST)

        if self.peekTokenIs(token.SEMICOLON):
            self.nextToken()
        
        return stmt

    # check the type of the current token
    def curTokenIs(self, t : str) -> bool:
        return self.curToken.type == t

    # check the type of the peek token
    def peekTokenIs(self, t : str) -> bool:
        return self.peekToken.type == t

    # assert the peek token
    def expectPeek(self, t : str) -> bool:
        if self.peekTokenIs(t):
            self.nextToken()
            return True
        
        self.peekError(t)
        return False
    
    # get list of errors
    def getErrors(self) -> List[str]:
        return self.errors
    
    # add error about the type of the next token
    def peekError(self, token : token.Token):
        msg = "expected next token to be {}, got {}".format(token, self.peekToken.type)
        self.errors.append(msg)

    # register prefix parsing function for tokenType
    def registerPrefix(self, tokenType : token.Token, fn : callable):
        self.prefixParseFns[tokenType] = fn
    
    # register infix parsing function for tokenType
    def registerInfix(self, tokenType : token.Token, fn : callable):
        self.infixParseFns[tokenType] = fn

    # parse expression statement
    def parseExpressionStatement(self) -> ast.Statement:
        stmt = ast.ExpressionStatement(self.curToken)
        stmt.expression = self.parseExpression(LOWEST)

        if self.peekTokenIs(token.SEMICOLON):
            self.nextToken()
        
        return stmt

    # parse expression
    def parseExpression(self, priority : int) -> ast.Expression:
        prefix = None

        # if the curToken has a prefix token function, get it and use it
        if self.curToken.type in self.prefixParseFns:
            prefix = self.prefixParseFns[self.curToken.type]
        
        # otherwise, something went wrong
        if prefix is None:
            self.noPrefixParseFnError(self.curToken.type)
            return None
         
        # get left expression through prefix()
        leftExp = prefix()

        # while peek token is not ';' and current prioriy < priority of peek token:
        while not self.peekTokenIs(token.SEMICOLON) and priority < self.peekPrecedence():
            infix = None 
            # if the curToken has an infix token function, get it and use it
            if self.peekToken.type in self.infixParseFns:
                infix = self.infixParseFns[self.peekToken.type]     
            
            # otherwise, return leftExpression
            if infix is None:
                return leftExp
            
            # go to the next token
            self.nextToken()

            # get left expression through infix(leftExp)
            leftExp = infix(leftExp)
    
        return leftExp

    # parse identifier
    def parseIdentifier(self) -> ast.Identifier:
        return ast.Identifier(self.curToken, self.curToken.literal)

    # parse integer literal
    def parseIntegerLiteral(self)  -> ast.IntegerLiteral:
        lit = ast.IntegerLiteral(self.curToken)

        try:
            lit.value = int(self.curToken.literal)
        except ValueError:
            msg = "could not parse {} as integer".format(self.curToken.literal)
            self.errors.append(msg)
            return None

        return lit

    # add error about no prefix function
    def noPrefixParseFnError(self, token : token.Token):
        msg = "no prefix parse function for {} found".format(token)
        self.errors.append(msg)
    
    # parse prefix expression
    def parsePrefixExpression(self) -> ast.PrefixExpression:
        expression = ast.PrefixExpression(self.curToken, self.curToken.literal)
        self.nextToken()
        expression.right = self.parseExpression(PREFIX)
        return expression

    # precedence of peekToken, if it has one
    def peekPrecedence(self) -> int:
        if self.peekToken.type in precedences:
            return precedences[self.peekToken.type]    
        return LOWEST

    # precedence of curToken, if it has one
    def curPrecedence(self) -> int:
        if self.curToken.type in precedences:
            return precedences[self.curToken.type]    
        return LOWEST
    
    # parse infix expression
    def parseInfixExpression(self, left : ast.Expression) -> ast.InfixExpression:
        expression = ast.InfixExpression(self.curToken, left, self.curToken.literal)
        precedence = self.curPrecedence()
        self.nextToken()
        expression.right = self.parseExpression(precedence)

        return expression

    # parse boolean
    def parseBoolean(self) -> ast.Boolean:
        return ast.Boolean(self.curToken, self.curTokenIs(token.TRUE))
    
    # parse grouped expression
    def parseGroupedExpression(self) -> ast.Expression:
        self.nextToken()
        exp = self.parseExpression(LOWEST)

        if not self.expectPeek(token.RPAREN):
            return None
        
        return exp
    
    # parse if expression
    def parseIfExpression(self) -> ast.IfExpression:
        expression = ast.IfExpression(self.curToken)

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
    
    # parse block statement
    def parseBlockStatement(self) -> ast.BlockStatement:
        block = ast.BlockStatement(self.curToken, [])

        self.nextToken()

        while not self.curTokenIs(token.RBRACE) and not self.curTokenIs(token.EOF):
            stmt = self.parseStatement()
            if stmt is not None:
                block.statements.append(stmt)
            self.nextToken()
        
        return block
    
    # parse function literal - declaration
    def parseFunctionLiteral(self) -> ast.FunctionLiteral:
        lit = ast.FunctionLiteral(self.curToken)
        if not self.expectPeek(token.LPAREN):
            return None
        
        lit.parameters = self.parseFunctionParameters()
    
        if not self.expectPeek(token.LBRACE):
            return None
        
        lit.body = self.parseBlockStatement()
    
        return lit
    
    # parse function paramenters
    def parseFunctionParameters(self) -> List[ast.Identifier]:
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
    
    # parse call expression
    def parseCallExpression(self, function : ast.Expression) -> ast.CallExpression:
        exp = ast.CallExpression(self.curToken, function)
        exp.arguments = self.parseExpressionList(')')
        return exp
    
    # parse call arguments
    def parseExpressionList(self, end : str) -> List[ast.Expression]:
        args = []

        if self.peekTokenIs(end):
            self.nextToken()
            return args
        
        self.nextToken()

        args.append(self.parseExpression(LOWEST))

        while self.peekTokenIs(token.COMMA):
            self.nextToken()
            self.nextToken()
            args.append(self.parseExpression(LOWEST))
        
        if not self.expectPeek(end):
            return None
        
        return args
    
    def parseStringLiteral(self) -> ast.Expression:
        return ast.StringLiteral(self.curToken, self.curToken.literal)
    
    def parseArrayLiteral(self) -> ast.Expression:
        array = ast.ArrayLiteral(self.curToken)
        array.elements = self.parseExpressionList(token.RBRACKET)
        return array
    
    def parseIndexExpression(self, left : ast.Expression) -> ast.Expression:
        exp = ast.IndexExpression(self.curToken, left)

        self.nextToken()

        exp.index = self.parseExpression(LOWEST)
        if not self.expectPeek(token.RBRACKET):
            return None
        return exp
    
    def parseHashLiteral(self) -> ast.Expression:
        hash = ast.HashLiteral(self.curToken)
    
        hash.pairs = {}

        while not self.peekTokenIs(token.RBRACE):
            self.nextToken()
            key = self.parseExpression(LOWEST)

            if not self.expectPeek(token.COLON):
                return None
            
            self.nextToken()

            value = self.parseExpression(LOWEST)
            hash.pairs[key] = value
        
            if not self.peekTokenIs(token.RBRACE) and not self.expectPeek(token.COMMA):
                return None
        
        if not self.expectPeek(token.RBRACE):
            return None
        
        return hash