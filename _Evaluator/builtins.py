from typing import List
import _Object.object as object
from _Evaluator.utils import newError

# get let of something which has a length: str or array
def _len(*args : List[object.Object]) -> object.Object:
    if len(args) != 1:
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if isinstance(args[0], object.String):
        return object.Integer(len(args[0].value))
    
    if isinstance(args[0], object.Array):
        return object.Integer(len(args[0].elements))
    
    return newError("argument to `len` not supported, got {}", args[0].type())

# get the first element of an array
def _first(*args : List[object.Object]) -> object.Object:
    if (len(args) != 1):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if args[0].type() != object.ARRAY_OBJ:
        return newError("argument to `first` must be ARRAY, got {}", args[0].type())
    
    return object.NULL if len(args[0].elements) == 0 else args[0].elements[0]

# get the last element of an array
def _last(*args : List[object.Object]) -> object.Object:
    if (len(args) != 1):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if args[0].type() != object.ARRAY_OBJ:
        return newError("argument to `last` must be ARRAY, got {}", args[0].type())
    
    return object.NULL if len(args[0].elements) == 0 else args[0].elements[len(args[0].elements)-1]

# get an array without the first one
def _rest(*args : List[object.Object]) -> object.Object:
    if (len(args) != 1):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if args[0].type() != object.ARRAY_OBJ:
        return newError("argument to `rest` must be ARRAY, got {}", args[0].type())
    
    if len(args[0].elements) == 0:
        return object.NULL
    
    return object.Array(args[0].elements[1:])

# append an element to an array
def _push(*args : List[object.Object]) -> object.Object:
    if (len(args) != 2):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if args[0].type() != object.ARRAY_OBJ:
        return newError("argument to `push` must be ARRAY, got {}", args[0].type())
    
    newElements = args[0].elements
    newElements.append(args[1])
    return object.Array(newElements)

# update the value of array[index]
def _update(*args : List[object.Object]) -> object.Object:
    if (len(args) != 3):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if args[0].type() != object.ARRAY_OBJ:
        return newError("first argument to `update` must be ARRAY, got {}", args[0].type())
    
    if args[1].type() != object.INTEGER_OBJ:
        return newError("second argument to `update` must be INTEGER, got {}", args[0].type())

    if args[1].value < 0 or args[1].value >= len(args[0].elements):
        return newError("index out of range")
    
    args[0].elements[args[1].value] = args[2]

    return object.NULL

# exit
def _exit(*args : List[object.Object]) -> object.Object:
    return object.EXIT

# printNNL (print without new line)
def _print(*args : List[object.Object]) -> object.Object:
    for elem in args:
        print(elem.inspect(), end="")
    return object.NULL

# print
def _printl(*args : List[object.Object]) -> object.Object:
    for elem in args:
        print(elem.inspect())
    return object.NULL

# get a string out of an object
def _str(*args : List[object.Object]) -> object.Object:
    if (len(args) != 1):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    return object.String(str(args[0].inspect()))

# get an int out of a str object
def _int(*args : List[object.Object]) -> object.Object:
    if (len(args) != 1):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if not isinstance(args[0], object.String):
        return object.NULL
    
    returnValue = object.Integer(None)

    if "." in args[0].value:
        try:
            returnValue.value = float(args[0].value)
        except ValueError:
            return object.NULL
    else:
        try:
            returnValue.value = int(args[0].value)
        except ValueError:
            return object.NULL
    
    return returnValue

def _input(*args : List[object.Object]) -> object.Object:
    str = input()
    return object.String(str)

builtins = {
    "len"    : object.Builtin(_len),
    "first"  : object.Builtin(_first),
    "last"   : object.Builtin(_last),
    "rest"   : object.Builtin(_rest),
    "push"   : object.Builtin(_push),
    "print"  : object.Builtin(_print),
    "printl" : object.Builtin(_printl),
    "update" : object.Builtin(_update),
    "exit"   : object.Builtin(_exit),
    "str"    : object.Builtin(_str),
    "int"    : object.Builtin(_int),
    "input"  : object.Builtin(_input),
}