from _Object.const import * 

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
    
## -------- var

TRUE  = Boolean(True)
FALSE = Boolean(False)
NULL  = Null()