from dataclasses import dataclass
import string
from _Token.const import *

# Class used to memorize a Token
@dataclass
class Token:
    type:       string  # Type of the Token (from _Token.const)
    literal:    string  # Literal value

# Dictionary of associations between keywords and Token's types
keywords = {
    "fn"    : FUNCTION,
    "let"   : LET,
    "true"  : TRUE,
    "false" : FALSE,
    "if"    : IF,   
    "else"  : ELSE,
    "return": RETURN
}

def newToken(tokenType, ch):
    return Token(tokenType, ch)

# Distinguish keywords from identifiers 
def lookupIdent(ident):
    if ident in keywords:
        return keywords[ident]
    
    return IDENT