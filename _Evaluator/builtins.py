from typing import List
import _Object.object as object
from _Evaluator.utils import newError

def _len(*args : List[object.Object]):
    if len(args) != 1:
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if isinstance(args[0], object.String):
        return object.Integer(len(args[0].value))
    
    if isinstance(args[0], object.Array):
        return object.Integer(len(args[0].elements))
    
    return newError("argument to `len` not supported, got {}", args[0].type())

def _first(*args : List[object.Object]):
    if (len(args) != 1):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if args[0].type() != object.ARRAY_OBJ:
        return newError("argument to `first` must be ARRAY, got {}", args[0].type())
    
    return object.NULL if len(args[0].elements) == 0 else args[0].elements[0]

def _last(*args : List[object.Object]):
    if (len(args) != 1):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if args[0].type() != object.ARRAY_OBJ:
        return newError("argument to `last` must be ARRAY, got {}", args[0].type())
    
    return object.NULL if len(args[0].elements) == 0 else args[0].elements[len(args[0].elements)-1]

def _rest(*args : List[object.Object]):
    if (len(args) != 1):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if args[0].type() != object.ARRAY_OBJ:
        return newError("argument to `rest` must be ARRAY, got {}", args[0].type())
    
    if len(args[0].elements) == 0:
        return object.NULL
    
    return object.Array(args[0].elements[1:])

def _push(*args : List[object.Object]):
    if (len(args) != 2):
        return newError("wrong number of arguments. got={}, want=1", len(args))
    
    if args[0].type() != object.ARRAY_OBJ:
        return newError("argument to `rest` must be ARRAY, got {}", args[0].type())
    
    newElements = args[0].elements
    newElements.append(args[1])
    return object.Array(newElements)

def _print(*args : List[object.Object]):
    for elem in args:
        print(elem.inspect())
    return object.NULL

builtins = {
    "len" : object.Builtin(_len),
    "first" : object.Builtin(_first),
    "last" : object.Builtin(_last),
    "rest" : object.Builtin(_rest),
    "push" : object.Builtin(_push),
    "print" : object.Builtin(_print),
}