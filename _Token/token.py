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
    "fn"        : FUNCTION,
    "let"       : LET,
    "true"      : TRUE,
    "false"     : FALSE,
    "if"        : IF,   
    "else"      : ELSE,
    "return"    : RETURN,
    "and"       : AND,
    "or"        : OR,
    "while"     : WHILE,
    "break"     : BREAK,
    "continue"  : CONTINUE,
    "for"       : FOR,
    "class"     : CLASS,
}

def newToken(tokenType : str, ch : str) -> Token:
    return Token(tokenType, ch)

# Distinguish keywords from identifiers 
def lookupIdent(ident : str) -> str:
    if ident in keywords:
        return keywords[ident]
    
    return IDENT