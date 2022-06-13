from typing import List
import _Ast.ast as ast
import _Object.object as object
import _Object.const as const

def Eval(node : ast.Node) -> object.Object:
    if isinstance(node, ast.Program):
        return evalStatement(node.statements)

    elif isinstance(node, ast.ExpressionStatement):
        return Eval(node.expression)

    elif isinstance(node, ast.IntegerLiteral):
        return object.Integer(node.value)

    elif isinstance(node, ast.Boolean):
        return nativeBoolToBooleanObject(node.value)

    elif isinstance(node, ast.PrefixExpression):
        right = Eval(node.right)
        return evalPrefixExpression(node.operator, right)

    elif isinstance(node, ast.InfixExpression):
        right = Eval(node.right)
        left  = Eval(node.left)
        return evalInfixExpression(node.operator, left, right)

    else:
        return None

def nativeBoolToBooleanObject(exp : bool) -> object.Object:
    return object.TRUE if exp else object.FALSE

def evalStatement(stmts : List[ast.Node]) -> object.Object:
    result = None
    for statement in stmts:
        result = Eval(statement)
    return result

def evalPrefixExpression(operator : str, right : object.Object) -> object.Object:
    if operator == "!":
        return evalBangOperatorExpression(right)
    elif operator == "-":
        return evalMinusPrefixOperatorExpression(right)
    else:
        return object.NULL
    
def evalBangOperatorExpression(right : object.Object) -> object.Object:
    if right == object.TRUE:
        return object.FALSE
    if right == object.FALSE:
        return object.TRUE
    if right == object.NULL:
        return object.TRUE
    return object.FALSE

def evalMinusPrefixOperatorExpression(right : object.Object) -> object.Object:
    if not isinstance(right, object.Integer):
        return object.NULL
    
    value = right.value
    return object.Integer(-value)

def evalInfixExpression(operator : str, left : object.Object, right : object.Object) -> object.Object:  
    if left.type() == object.INTEGER_OBJ and right.type() == object.INTEGER_OBJ:
        return evalIntegerInfixExpression(operator, left, right)
    if operator == "==":
        return nativeBoolToBooleanObject(left == right)
    if operator == "!=":
        return nativeBoolToBooleanObject(left != right)
    else:
        return object.NULL

def evalIntegerInfixExpression(operator : str, left : object.Object, right : object.Object) -> object.Object:  
    leftValue = left.value
    rightValue = right.value

    if operator == "+":
        return object.Integer(leftValue + rightValue)
    if operator == "-":
        return object.Integer(leftValue - rightValue)
    if operator == "*":
        return object.Integer(leftValue * rightValue)
    if operator == "/":
        return object.Integer(leftValue / rightValue)
    if operator == "<":
        return nativeBoolToBooleanObject(leftValue < rightValue)
    if operator == ">":
        return nativeBoolToBooleanObject(leftValue > rightValue)
    if operator == "==":
        return nativeBoolToBooleanObject(leftValue == rightValue)
    if operator == "!=":
        return nativeBoolToBooleanObject(leftValue != rightValue)
    
    return object.NULL