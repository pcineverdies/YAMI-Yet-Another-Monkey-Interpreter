
from typing import List
import copy
import _Ast.ast as ast
import _Object.object as object
import _Evaluator.builtins as builtins
from _Evaluator.utils import newError

# main evaluator (recursive) function: depending on the curret ast.node,
# it calls different functions
def Eval(node : ast.Node, env : object.Environment) -> object.Object:
    # case of the program, as an array of statements
    if isinstance(node, ast.Program):
        return evalProgram(node.statements, env)

    # case of an expression
    elif isinstance(node, ast.ExpressionStatement):
        return Eval(node.expression, env)

    # case of an integer literal
    elif isinstance(node, ast.IntegerLiteral):
        return object.Integer(node.value)

    # case of a boolean
    elif isinstance(node, ast.Boolean):
        return nativeBoolToBooleanObject(node.value)

    # case of a prefix expression
    elif isinstance(node, ast.PrefixExpression):
        # first: eval the right expression
        right = Eval(node.right, env)
        if isError(right):
            return right

        # second: apply the prefix operator
        return evalPrefixExpression(node.operator, right)

    # case of infix expression
    elif isinstance(node, ast.InfixExpression):
        if node.operator == ".":
            return evalClassInstanceExpression(node, env)

        # first: eval the right expression
        right = Eval(node.right, env)
        if isError(right):
            return right

        # second: eval the left expression
        left  = Eval(node.left, env)
        if isError(left):
            return left

        # third: apply the operator
        return evalInfixExpression(node.operator, left, right)
    
    # case of a block statement (eval eash stmt)
    elif isinstance(node, ast.BlockStatement):
        return evalBlockStatements(node, env)
    
    # case of an if statement (eval consequence depending on condition)
    elif isinstance(node, ast.IfExpression):
        return evalIfExpression(node, env)
    
    elif isinstance(node, ast.WhileExpression):
        return evalWhileExpression(node, env)

    elif isinstance(node, ast.ForExpression):
        return evalForExpression(node, env)
    
    # case of a return statement
    elif isinstance(node, ast.ReturnStatement):
        if node.value is None:
            return object.ReturnValue(object.Integer(0))

        val = Eval(node.value, env)
        if isError(val):
            return val

        return object.ReturnValue(val)
    
    # case of a let statement
    elif isinstance(node, ast.LetStatement):
        val = Eval(node.value, env)
        if isError(val):
            return val
        
        if node.instance is not None:
            instance, exist = env.get(node.name.value)
            if not exist or not isinstance(instance, object.ClassInstance):
                return newError("Can't find object {}", node.name.value)
            _, exist = instance.env.get(node.instance.value)
            if not exist:
                return newError("Can't find instance {}", node.instance.value)
            instance.env.set(node.instance.value, val, True)
            return

        # set the current enviroment value
        env.set(node.name.value, val, True)
    
    # case of an identifier (get its value from env)
    elif isinstance(node, ast.Identifier):
        return evalIdentifier(node, env)
    
    # case of a function literal
    elif isinstance(node, ast.FunctionLiteral):
        params = node.parameters
        body = node.body
        return object.Function(params, body)
    
    # case of a call expression
    elif isinstance(node, ast.CallExpression):
        # eval the function
        function = Eval(node.function, env)
        if isError(function):
            return function
        
        if(isinstance(function, object.Class)):
            return object.ClassInstance(copy.deepcopy(function.env))
        
        # eval its arguments
        args = evalExpressions(node.arguments, env)
        if len(args) == 1 and isError(args[0]):
            return args[0]

        # apply the function
        return applyFunction(function, args, env)
    
    # case of string
    elif isinstance(node, ast.StringLiteral):
        return object.String(node.value)

    # array literals
    elif isinstance(node, ast.ArrayLiteral):
        elements = evalExpressions(node.elements, env)
        if len(elements) == 1 and isError(elements[0]):
            return elements[0]
        return object.Array(elements)

    # index expression
    elif isinstance(node, ast.IndexExpression):
        left = Eval(node.left, env)
        if isError(left):
            return left
        
        index = Eval(node.index, env)
        if isError(index):
            return index
        
        return evalIndexExpression(left, index)
    
    # hash literal
    elif isinstance(node, ast.HashLiteral):
        return evalHashLiteral(node, env)

    # case of assign statement
    elif isinstance(node, ast.AssignStatement):
        val = Eval(node.value, env)
        if isError(val):
            return val
        
        # set the current enviroment value
        value, ok = env.get(node.name.value)
        if not ok:
            return newError("Can't assign value before declaration")
        env.set(node.name.value, val, False)
    
    elif isinstance(node, ast.ContinueStatement):
        if not env.inLoop:
            return newError("Can't use continue outside a loop")
        return object.CONTINUE

    elif isinstance(node, ast.BreakStatement):
        if not env.inLoop:
            return newError("Can't use break outside a loop")
        return object.BREAK
    
    elif isinstance(node, ast.Classliteral):
        return evalClassLiteral(node)

    # no functino to eval the ast.node
    else:
        return None

# return the corresponding instance of object.Object
def nativeBoolToBooleanObject(exp : bool) -> object.Object:
    return object.TRUE if exp else object.FALSE

# eval prefix expression depending on the operator
def evalPrefixExpression(operator : str, right : object.Object) -> object.Object:
    if operator == "!":
        return evalBangOperatorExpression(right)
    elif operator == "-":
        return evalMinusPrefixOperatorExpression(right)
    else:
        return newError("unknwon operator: {}{}", operator, right.type())

# eval the bang operator
def evalBangOperatorExpression(right : object.Object) -> object.Object:
    if right in [object.FALSE, object.NULL]:
        return object.TRUE
    return object.FALSE

# eval the minus prefix operator
def evalMinusPrefixOperatorExpression(right : object.Object) -> object.Object:
    if not isinstance(right, object.Integer):
        return newError("unknown operator: -{}", right.type())
    
    value = right.value
    return object.Integer(-value)

# eval infix expression: get the vlaues of left and right and apply the python's correspondant operator
def evalInfixExpression(operator : str, left : object.Object, right : object.Object) -> object.Object:  
    # case of both integers
    if left.type() == object.INTEGER_OBJ and right.type() == object.INTEGER_OBJ:
        return evalIntegerInfixExpression(operator, left, right)
    
    if left.type() == object.STRING_OBJ and right.type() == object.STRING_OBJ:
        return evalStringInfixExpression(operator, left, right)
    
    if operator == "==":
        return nativeBoolToBooleanObject(left == right)
    if operator == "!=":
        return nativeBoolToBooleanObject(left != right)
    if operator == "&&" or operator == "and":
        return nativeBoolToBooleanObject(left.value and right.value)
    if operator == "||" or operator == "or":
        return nativeBoolToBooleanObject(left.value or  right.value)
    if left.type() != right.type():
        return newError("type mismatch: {} {} {}", left.type(), operator, right.type())
    else:
        return newError("unknown operator: {} {} {}", left.type(), operator, right.type())

# eval integer infix expression
def evalIntegerInfixExpression(operator : str, left : object.Object, right : object.Object) -> object.Object:  
    leftValue = left.value
    rightValue = right.value

    if operator == "+":
        return object.Integer(leftValue + rightValue)
    if operator == "-":
        return object.Integer(leftValue - rightValue)
    if operator == "*":
        return object.Integer(leftValue * rightValue)
    # in case of integers, '/' is the division between integers
    if operator == "/":
        return object.Integer(leftValue / rightValue)
    if operator == "%":
        return object.Integer(leftValue %  rightValue)
    if operator == "<":
        return nativeBoolToBooleanObject(leftValue <  rightValue)
    if operator == ">":
        return nativeBoolToBooleanObject(leftValue >  rightValue)
    if operator == "<=":
        return nativeBoolToBooleanObject(leftValue <= rightValue)
    if operator == ">=":
        return nativeBoolToBooleanObject(leftValue >= rightValue)
    if operator == "==":
        return nativeBoolToBooleanObject(leftValue == rightValue)
    if operator == "!=":
        return nativeBoolToBooleanObject(leftValue != rightValue)
    
    return newError("unknown operator: {} {} {}", left.type(), operator, right.type())

# eval if expression
def evalIfExpression(ie : ast.IfExpression, env: object.Environment) -> object.Object:
    # eval condition
    newEnv = object.Environment(env, env.inLoop)

    condition = Eval(ie.condition, env)
    if isError(condition):
        return condition
    
    # if condition is true, eval consequence
    if isTruthy(condition):
        return Eval(ie.consequence, newEnv)
    
    # else if there's else branch, eval it
    elif ie.alternative is not None:
        return Eval(ie.alternative, newEnv)
    
    # else return NULL
    else:
        return object.NULL

def isTruthy(obj : object.Object) -> bool:
    if obj in [object.FALSE, object.NULL]:
        return False
    return True

# eval each statement of the program
def evalProgram(program : ast.Program, env : object.Environment) -> object.Object:
    result = None
    for statement in program:
        # refresh the result value for each statement, so that that last statement
        # give the return value of the block
        result = Eval(statement, env)

        # if we encounter a return statement, we don't want to go on
        if isinstance(result, object.ReturnValue):
            return result.value
        elif isinstance(result, (object.Exit, object.Error)):
            return result
    return result

# eval each statement of the block
def evalBlockStatements(block : ast.BlockStatement, env : object.Environment) -> object.Object:
    result = None
    for statement in block.statements:
        result = Eval(statement, env)

        if result is not None:
            if result.type() in [object.BREAK_OBJ, object.CONTINUE_OBJ, object.RETURN_VALUE_OBJ, object.ERROR_OBJ, object.EXIT_OBJ]:
                return result

    return result

def isError(obj : object.Object) -> bool:
    if obj is not None:
        return obj.type() == object.ERROR_OBJ
    return False

# get the identifer from the current env
def evalIdentifier(node : ast.Identifier, env : object.Environment) -> object.Object:
    val, ok = env.get(node.value)
    if ok:
        return val
    
    if node.value in builtins.builtins:
        return builtins.builtins[node.value]

    return newError("identifier not found: " + node.value)


# eval expressions as input of function call
def evalExpressions(exps : List[ast.Expression], env : object.Object) -> List[object.Object]:
    result = []

    for elem in exps:
        evaluated = Eval(elem, env)
        if isError(evaluated):
            return [evaluated]
        result.append(evaluated)
    
    return result

# apply a function
def applyFunction(fn : object.Object, args : List[object.Object], env : object.Environment = None) -> object.Object:
    if isinstance(fn, object.Function):
    # we extended the environment of a function pushing the arguments too
        if len(fn.parameters) != len(args):
            return newError("wrong number of parametrs: wanted {}, got {}", len(fn.parameters), len(args))
        extendedEnv = extendFunctionEnvironment(fn, args, env)
        evaluated = Eval(fn.body, extendedEnv)
        return unwrapReturnValue(evaluated)
    
    if isinstance(fn, object.Builtin):
        return fn.fn(*args)
    
    return newError("not a function: {}", fn.type())

# extend function environment
def extendFunctionEnvironment(fn : object.Object, args : List[object.Object], env : object.Environment = None) -> object.Environment:
    env = object.Environment(env)

    for idx, param in enumerate(fn.parameters):
        env.set(param.value, args[idx], True)

    return env

def unwrapReturnValue(ev : object.Object) -> object.Object:
    if isinstance(ev, object.ReturnValue):
        return ev.value
    
    return ev

def evalStringInfixExpression(operator : str, left : object.Object, right : object.Object) -> object.Object:
    if operator not in ["+", "==", "!="]:
        return newError("unknown operator: {} {} {}", left.type(), operator, right.type())
    
    leftVal = left.value
    rightVal = right.value
    if operator == "+":
        return object.String(leftVal + rightVal)
    elif operator == "!=":
        return nativeBoolToBooleanObject(leftVal != rightVal)
    elif operator == "==":
        return nativeBoolToBooleanObject(leftVal == rightVal)


def evalIndexExpression(left : object.Object, index : object.Object) -> object.Object:
    if left.type() == object.ARRAY_OBJ and index.type() == object.INTEGER_OBJ:
        return evalArrayIndexExpression(left, index)
    
    if left.type() == object.HASH_OBJ:
        return evalHashIndexExpression(left, index)
    
    return newError("index operator not supported: {}",format(left.type()))

def evalArrayIndexExpression(array : object.Object, index : object.Object) -> object.Object:
    idx = index.value
    max = int(len(array.elements)-1)

    if idx < 0 or idx > max:
        return object.NULL
    
    return array.elements[idx]

def evalHashLiteral(node : ast.HashLiteral, env : object.Environment) -> object.Object:
    pairs = {}

    for keyNode, valueNode in node.pairs.items():
        key = Eval(keyNode, env)
        if isError(key):
            return key
        
        if not isinstance(key, object.Hashable):
            return newError("unusable as hash key: {}".format(key.type()))
        
        value = Eval(valueNode, env)
        if isError(value):
            return value

        hashed = key.hashKey()
        pairs[hashed] = object.HashPair(key, value)
    
    return object.Hash(pairs)

def evalHashIndexExpression(left : object.Object, index : object.Object) -> object.Object:
    if not isinstance(index, object.Hashable):
        return newError("unusable as hash key: {}".format(index.type()))
    
    if index.hashKey() in left.pairs:
        return left.pairs[index.hashKey()].value
    
    return object.NULL

# eval while expression
def evalWhileExpression(we : ast.WhileExpression, env: object.Environment) -> object.Object:
    result = object.NULL
    newEnv = object.Environment(env, True)
    while True:
        condition = Eval(we.condition, env)
        if isError(condition):
            return condition
    
        # if condition is true, eval consequence
        if isTruthy(condition):
            result = Eval(we.block, newEnv)
            if isinstance(result, (object.Break)):
                return object.NULL
            elif isinstance(result, (object.Error, object.Exit, object.ReturnValue)):
                return result
            elif isinstance(result, object.Continue):
                result = object.NULL
                continue
        else:
            return result


def evalForExpression(floop : ast.ForExpression, env : object.Environment) -> object.Object:
    # result of the for loop -> result of last statemnet executed
    result = object.NULL
    # remember if we were in a loop
    newEnv = object.Environment(env, True)

    # if there is an initial statement
    if floop.initial is not None:
        initial = Eval(floop.initial, newEnv)
        if isError(initial):
            return initial
    
    while True:
        condition = object.TRUE
        # check condition of floop
        if floop.condition is not None:
            condition = Eval(floop.condition, newEnv)
            if isError(condition):
                return condition

        if isTruthy(condition):
            # eval block
            result = Eval(floop.block, newEnv)

            # case of a result type which stops the loop
            if isinstance(result, (object.Error, object.Exit, object.ReturnValue, object.Break)):
                # return NULL if it was an object.Break
                return object.NULL if isinstance(result, object.Break) else result

            if floop.update is not None:
                update = Eval(floop.update, newEnv)
                if isError(update):
                    return update
            
            if isinstance(result, object.Continue):
                result = object.NULL

        else:
            return result

def evalClassLiteral(classLiteral : ast.Classliteral) -> object.Object:
    newClass = object.Class(classLiteral.body, object.Environment(None, False))
    for statement in classLiteral.body.statements:
        if not isinstance(statement, ast.LetStatement):
            return newError("in class declaration there must be only Let statements")
        _ = Eval(statement, newClass.env)
    return newClass

def evalClassInstanceExpression(node : ast.InfixExpression, env : object.Environment) -> object.Object:
    if not isinstance(node.left, ast.Identifier) or not node.operator == ".":
        return newError("Can't find a way to execute DOT operator")
    
    classInst, exist = env.get(node.left.value)
    if not exist or not isinstance(classInst, object.ClassInstance):
        return newError("{} does not exist in current scope", node.left.value)
    
    if isinstance(node.right, ast.Identifier):
        identifierName = node.right.value
        identifier, exist = classInst.env.get(identifierName)
        return identifier

    elif isinstance(node.right, ast.CallExpression):
        # eval the function
        function = Eval(node.right.function, classInst.env)
        if isError(function):
            return function
        
        if(isinstance(function, object.Class)):
            return object.ClassInstance(function.env)
        
        args = evalExpressions(node.right.arguments, env)
        if len(args) == 1 and isError(args[0]):
            return args[0]

        # apply the function
        return applyFunction(function, args, classInst.env)
    
    else:
        return newError("Can't find a way to execute DOT operator")

