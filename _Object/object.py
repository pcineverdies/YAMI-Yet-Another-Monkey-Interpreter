from __future__ import annotations
from _Object.const import * 
from typing import List, Tuple
import _Ast.ast as ast

class Object:
    
    def type(self) -> str:
        pass

    def insepct(self) -> str:
        pass

class Integer(Object):
    def __init__(self, value : int):
        self.value = value
    
    def insepct(self) -> str:
        return str(self.value)
    
    def type(self) -> str:
        return INTEGER_OBJ
    
class Boolean(Object):
    def __init__(self, value : bool):
        self.value = value
    
    def type(self) -> str:
        return BOOLEAN_OBJ
    
    def insepct(self) -> str:
        return "true" if self.value else "false"
    
class Null(Object):
    def type(self) -> str:
        return NULL_OBJ
    
    def insepct(self) -> str:
        return "null"

class ReturnValue(Object):
    def __init__(self, value : Object):
        self.value = value

    def type(self) -> str:
        return RETURN_VALUE_OBJ
    
    def insepct(self) -> str:
        return self.value.inspect

class Error(Object):
    def __init__(self, message : str):
        self.message = message
    
    def type(self) -> str:
        return ERROR_OBJ
    
    def insepct(self) -> str:
        return "ERROR: " + self.message

class Function:
    def __init__(self, parameters : List[ast.Identifier], body : ast.BlockStatement, env : Environment):
        self.parameters = parameters
        self.body = body
        self.env = env
    
    def type(self) -> Object:
        return FUNCTION_OBJ
    
    def inspect(self) -> str:
        params = []
        for elem in self.parameters:
            params.append(elem.string())

        return "fn(" + ", ".join(params) + ") {\n" + self.body.string() + "\n}"

class Environment:
    def __init__(self, outer : Environment = None):
        self.store = {}
        self.outer = outer

    
    def get(self, name : str) -> Tuple[Object, bool]:
        if name in self.store:
            return self.store[name], True
        elif self.outer is not None:
            return self.outer.get(name)
        else:
            return None, False
    
    def set(self, name : str, value : Object) -> Object:
        self.store[name] = value
        return value

TRUE  = Boolean(True)
FALSE = Boolean(False)
NULL  = Null()