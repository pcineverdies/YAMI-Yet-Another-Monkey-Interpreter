import _Token.token as token

class Node:
    def tokenLiteral(self):
        pass
    def string(self):
        pass

class Statement(Node):
    def statementNode(self):
        pass

class Expression(Node):
    def expressionNode(self):
        pass

class Program:
    def __init__(self):
        self.statements = []
    
    def tokenLiteral(self):
        if len(self.statements) > 0:
            return self.statements[0].tokenLiteral()
        
        else:
            return ""
    
    def string(self):
        out = ""

        for s in self.statements:
            out = out + s.string()
        
        return out

class Identifier(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        return self.value

class LetStatement(Statement):
    def __init__(self, token, name, value):
        self.token = token
        self.name = name
        self.value = value

    def statementNode(self):
        return super().statementNode()
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        msg = ""
        msg += self.tokenLiteral() + " "
        msg += self.name.string() + " = "

        if self.value != None:
            msg += self.value.string()
        
        msg += ";"

        return msg

class ReturnStatement(Statement):
    def __init__(self, token, returnValue):
        self.token = token
        self.returnValue = returnValue
        
    def statementNode(self):
        return super().statementNode()
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        msg = ""
        msg += self.tokenLiteral() + " "

        if self.value != None:
            msg += self.value.string()
        
        msg += ";"

        return msg

class ExpressionStatement(Statement):
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression
    
    def statementNode(self):
        return super().statementNode()
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        if self.expression != None:
            return self.expression.string()
        
        return ""

class IntegerLiteral(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self):
        return self.token.literal

    def string(self):
        return self.token.literal

