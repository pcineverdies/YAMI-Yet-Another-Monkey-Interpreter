from __future__ import annotations
from _Object.const import * 
from typing import Callable, Dict, List, Tuple
import _Ast.ast as ast
import hashlib

class Object:
    def type(self) -> str:
        pass

    def inspect(self) -> str:
        pass

class Hashable:
    def hashKey() -> int:
        pass

class Integer(Object, Hashable):
    def __init__(self, value : int):
        self.value = value
    
    def inspect(self) -> str:
        return str(self.value)
    
    def type(self) -> str:
        return INTEGER_OBJ

    def hashKey(self) -> int:
        return self.value
    
class Boolean(Object, Hashable):
    def __init__(self, value : bool):
        self.value = value
    
    def type(self) -> str:
        return BOOLEAN_OBJ
    
    def inspect(self) -> str:
        return "true" if self.value else "false"
    
    def hashKey(self) -> int:
        value = 1 if self.value else 0
        return value
    
class Null(Object):
    def type(self) -> str:
        return NULL_OBJ
    
    def inspect(self) -> str:
        return "null"

class ReturnValue(Object):
    def __init__(self, value : Object):
        self.value = value

    def type(self) -> str:
        return RETURN_VALUE_OBJ
    
    def inspect(self) -> str:
        return self.value.inspect

class Error(Object):
    def __init__(self, message : str):
        self.message = message
    
    def type(self) -> str:
        return ERROR_OBJ
    
    def inspect(self) -> str:
        return "ERROR: " + self.message

class Function(Object):
    def __init__(self, parameters : List[ast.Identifier], body : ast.BlockStatement):
        self.parameters = parameters
        self.body = body
    
    def type(self) -> Object:
        return FUNCTION_OBJ
    
    def inspect(self) -> str:
        params = []
        for elem in self.parameters:
            params.append(elem.string())

        return "fn(" + ", ".join(params) + ") {\n" + self.body.string() + "\n}"

class Environment:
    def __init__(self, outer : Environment = None, inLoop : bool = False):
        self.store = {}
        self.outer = outer
        self.inLoop = inLoop
    
    def get(self, name : str) -> Tuple[Object, bool]:
        if name in self.store:
            return self.store[name], True
        elif self.outer is not None:
            return self.outer.get(name)
        else:
            return None, False
    
    def set(self, name : str, value : Object, inCurrentSope : bool):
        if self.get(name)[1] and not inCurrentSope:
            if name in self.store:
                self.store[name] = value
                return
            else:
                self.outer.set(name, value, inCurrentSope)
        else:
            self.store[name] = value

    def reset(self, name : str):
        self.store.pop(name)

class String(Object, Hashable):
    def __init__(self, value : str):
        self.value = value
    
    def type(self) -> str:
        return STRING_OBJ
    
    def inspect(self) -> str:
        return self.value
    
    def hashKey(self) -> int:
        return int.from_bytes(hashlib.sha256(self.value.encode("ASCII")).digest()[:8], "little")
        

class Builtin(Object):
    def __init__(self, fn : Callable):
        self.fn = fn

    def type(self) -> str:
        return BUILTIN_OBJ
    
    def inspect(self) -> str:
        return "builtin function"

class Array(Object):
    def __init__(self, elements : List[Object] = None):
        self.elements = elements
    
    def type(self) -> Object:
        return ARRAY_OBJ
    
    def inspect(self) -> str:
        elements = []
        for elem in self.elements:
            elements.append(elem.inspect())
        
        return "[" + ", ".join(elements) + "]"

class HashPair:
    def __init__(self, key : Object, value : Object = None):
        self.key = key
        self.value = value

class Hash(Object):
    def __init__(self, pairs : Dict = None):
        self.pairs = pairs

    def type(self) -> str:
        return HASH_OBJ

    def inspect(self) -> str:
        pairs = []

        for elem in self.pairs.values():
            pairs.append("{} : {}".format(elem.key.inspect(), elem.value.inspect()))
        
        return "{" + ", ".join(pairs) + "}"

class Exit(Object):
    def type(self) -> str:
        return EXIT_OBJ

    def inspect(self) -> str:
        return "program exited"

class Break(Object):
    def type(self) -> str:
        return BREAK_OBJ

    def inspect(self) -> str:
        return BREAK_OBJ

class Continue(Object):
    def type(self) -> str:
        return CONTINUE_OBJ

    def inspect(self) -> str:
        return CONTINUE_OBJ

class Class(Object):
    def __init__(self, body : ast.BlockStatement = None, env : Environment = None):
        self.env = env
        self.body = body # used just to print it
    
    def type(self) -> Object:
        return CLASS_OBJ

class ClassInstance(Object):
    def __init__(self, env : Environment):
        self.env = env

    def type(self) -> str:
        return CLASS_INSTANCE_OBJ
    
    def inspect(self) -> str:
        return CLASS_INSTANCE_OBJ

TRUE     = Boolean(True)
FALSE    = Boolean(False)
EXIT     = Exit()
NULL     = Null()
BREAK    = Break()
CONTINUE = Continue()
