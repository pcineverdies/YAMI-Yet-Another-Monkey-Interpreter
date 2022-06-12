from lib2to3.pgen2.token import LESS
import _Token.token as token

LOWEST          = 0
EQUALS          = 1 
LESSGREATER     = 2
SUM             = 3
PRODUCT         = 4
PREFIX          = 5
CALL            = 6

precedences = {
    token.EQ        : EQUALS,
    token.NOT_EQ    : EQUALS,
    token.LT        : LESSGREATER,
    token.GT        : LESSGREATER,
    token.PLUS      : SUM,
    token.MINUS     : SUM,
    token.SLASH     : PRODUCT,
    token.ASTERISK  : PRODUCT,
}