from typing import List, Dict
import _Token.token as token

# Abstract class for a Node in AST
class Node:
    def tokenLiteral(self) -> str:
        pass
    def string(self) -> str:
        pass

# Abstract class for a Statement in AST
class Statement(Node):
    def statementNode(self):
        pass

# Abstract class for an Expression in AST
class Expression(Node):
    def expressionNode(self):
        pass

# Program as a collection of statements
class Program:
    def __init__(self):
        self.statements = []
    
    def tokenLiteral(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].tokenLiteral()
        
        else:
            return ""
    
    def string(self) -> str:
        out = ""

        for s in self.statements:
            out = out + s.string()
        
        return out

# Identifier node
class Identifier(Expression):
    def __init__(self, token : token.Token, value):
        self.token = token
        self.value = value
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        return self.value

# LetStatement node
class LetStatement(Statement):
    def __init__(self, token : token.Token, name : Identifier = None, 
                 value : Expression = None):
        self.token = token
        self.name = name
        self.value = value

    def statementNode(self):
        return super().statementNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        msg = ""
        msg += self.tokenLiteral() + " "
        msg += self.name.string() + " = "

        if self.value != None:
            msg += self.value.string()
        
        msg += ";"

        return msg

# ReturnStatement node
class ReturnStatement(Statement):
    def __init__(self, token : token.Token = None, 
                 value : Expression = None):
        self.token = token
        self.value = value
        
    def statementNode(self):
        return super().statementNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        msg = ""
        msg += self.tokenLiteral() + " "

        if self.value != None:
            msg += self.value.string()
        
        msg += ";"

        return msg

# ExpressionStatement node
class ExpressionStatement(Statement):
    def __init__(self, token : token.Token, 
                 expression : Expression = None):
        self.token = token
        self.expression = expression
    
    def statementNode(self):
        return super().statementNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        if self.expression != None:
            return self.expression.string() + ";"
        
        return ""

# IntegerLiteral node
class IntegerLiteral(Expression):
    def __init__(self, token : token.Token, 
                 value : int = None):
        self.token = token
        self.value = value
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.token.literal

# PrefixExpression node
class PrefixExpression(Expression):
    def __init__(self, token : token.Token, 
                 operator : str = None, right : Expression = None):
        self.token = token
        self.operator = operator
        self.right = right
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        return "(" + self.operator + self.right.string() + ")"

# InfixExpression node
class InfixExpression(Expression):
    def __init__(self, token : token.Token, left : Expression = None, 
                 operator : str = None, right : Expression = None):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        return "(" + self.left.string() + " " + self.operator + " " + self.right.string() + ")"
    
# Boolean node
class Boolean(Expression):
    def __init__(self, token : token.Token, 
                 value : bool = None):
        self.token = token
        self.value = value
        
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        return self.token.literal

# BlockStatement node (colletion of statements)
class BlockStatement(Statement):
    def __init__(self, token, statements = None):
        self.token = token
        self.statements = statements
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        out = "{"
        stmts = []
        for elem in self.statements:
            stmts.append(elem.string())
        out += " ".join(stmts)
        out += "}"
        return out 
    
# IfExpression node
class IfExpression(Expression):
    def __init__(self, token : token.Token, condition : Expression = None, 
                 consequence : BlockStatement = None, alternative : BlockStatement = None):
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.litearl
    
    def string(self) -> str:
        out = "if" + self.condition.string() + " " + self.consequence.string()
        if self.alternative is not None:
            out += "else " + self.alternative.string()
        
        return out

# FunctionLiteral node
class FunctionLiteral(Expression):
    def __init__(self, token : token.Token, 
                 parameters : List[Identifier] = None, body : BlockStatement = None):
        self.token = token
        self.parameters = parameters
        self.body = body
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        params = []
        for p in self.parameters:
            params.append(p.string())

        out  = self.tokenLiteral() + "(" + ", ".join(params) + ") "
        out += self.body.string()

        return out
    
# CallExpression node
class CallExpression(Expression):
    def __init__(self, token : token.Token, 
                 function : Expression = None, arguments : List[Expression] = None):
        self.token = token
        self.function = function
        self.arguments = arguments
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        args = []
        for elem in self.arguments:
            args.append(elem.string())
        
        out = self.function.string()
        out += "("
        out += ", ".join(args)
        out += ")"

        return out
    
class StringLiteral(Expression):
    def __init__(self, token : token.Token, value : str = None):
        self.token = token
        self.value = value
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        return self.token.literal

class ArrayLiteral(Expression):
    def __init__(self, token : token.Token, elements : List[Expression] = None):
        self.token = token
        self.elements = elements
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        elements = []
        for elem in self.elements:
            elements.append(elem.string())
        
        return "[" + ", ".join(elements) + "]"

class IndexExpression(Expression):
    def __init__(self, token : token.Token, left : Expression = None, index : Expression = None):
        self.token = token
        self.left = left
        self.index = index
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self):
        return "(" + self.left.string() + "[" + self.index.string() + "])"
    
class HashLiteral(Expression):
    def __init__(self, token : token.Token, pairs : Dict = None):
        self.token = token
        self.pairs = pairs
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        pairs = []
        for key, value in self.pairs.items():
            pairs.append(key.string() + ":" + value.string())
        
        return "{" + ", ".join(pairs) + "}"

class WhileExpression(Expression):
    def __init__(self, token : token.Token, condition : Expression = None, block : BlockStatement = None):
        self.token = token
        self.condition = condition
        self.block = block
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.litearl
    
    def string(self) -> str:
        return "while" + self.condition.string() + " " + self.consequence.string()

# Assign statement node
class AssignStatement(Statement):
    def __init__(self, token : token.Token, name : Identifier = None, 
                 value : Expression = None):
        self.token = token
        self.name = name
        self.value = value

    def statementNode(self):
        return super().statementNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        msg = self.name.string() + " = "

        if self.value != None:
            msg += self.value.string()
        
        msg += ";"

        return msg

# Break statement
class BreakStatement(Statement):

    def statementNode(self):
        return super().statementNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        return "break;"

# Continue statement
class ContinueStatement(Statement):

    def statementNode(self):
        return super().statementNode()
    
    def tokenLiteral(self) -> str:
        return self.token.literal
    
    def string(self) -> str:
        return "continue;"

class ForExpression(Expression):
    def __init__(self, token : token.Token, initial : Statement = None, condition : Expression = None,
                 update : Statement = None, block : BlockStatement = None):
        self.token = token
        self.initial = initial
        self.condition = condition
        self.update = update
        self.block = block
    
    def expressionNode(self):
        return super().expressionNode()
    
    def tokenLiteral(self) -> str:
        return self.token.litearl
    
    def string(self) -> str:
        out = "for( "
        if self.initial is not None:
            out += self.initial.string()
        out += "; "
        if self.condition is not None:
            out += self.condition.string()
        out += "; "
        if self.update is not None:
            out += self.update.string()
        out += ")" + self.block.string()
        return out