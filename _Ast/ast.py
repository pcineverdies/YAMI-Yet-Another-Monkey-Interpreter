from ast import operator
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
    def __init__(self, token, value):
        self.token = token
        self.value = value
        
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
            return self.expression.string() + ";"
        
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

class PrefixExpression(Expression):
    def __init__(self, token, operator, right):
        self.token = token
        self.operator = operator
        self.right = right
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        return "(" + self.operator + self.right.string() + ")"

class InfixExpression(Expression):
    def __init__(self, token, left, operator, right):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        return "(" + self.left.string() + " " + self.operator + " " + self.right.string() + ")"
    
class Boolean(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value
        
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        return self.token.literal
    
class IfExpression(Expression):
    def __init__(self, token, condition, consequence, alternative):
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self):
        return self.token.litearl
    
    def string(self):
        out = "if" + self.condition.string() + " " + self.consequence.string()
        if self.alternative is not None:
            out += "else " + self.alternative.string()
        
        return out
    
class BlockStatement(Statement):
    def __init__(self, token, statements):
        self.token = token
        self.statements = statements
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        out = "{"
        stmts = []
        for elem in self.statements:
            stmts.append(elem.string())
        out += " ".join(stmts)
        out += "}"
        return out 
    
class FunctionLiteral(Expression):
    def __init__(self, token, parameters, body):
        self.token = token
        self.parameters = parameters
        self.body = body
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        params = []
        for p in self.parameters:
            params.append(p.string())

        out  = self.tokenLiteral() + "(" + ", ".join(params) + ") "
        out += self.body.string()

        return out
    
class CallExpression(Expression):
    def __init__(self, token, function, arguments):
        self.token = token
        self.function = function
        self.arguments = arguments
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self):
        return self.token.literal
    
    def string(self):
        args = []
        for elem in self.arguments:
            args.append(elem.string())
        
        out = self.function.string()
        out += "("
        out += ", ".join(args)
        out += ")"

        return out