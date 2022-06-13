import _Token.token as token

# List of priorities 
LOWEST          = 0
EQUALS          = 1 
LESSGREATER     = 2
SUM             = 3
PRODUCT         = 4
PREFIX          = 5
CALL            = 6

# Dictionary that associates each token type
# to its priority
precedences = {
    token.EQ        : EQUALS,
    token.NOT_EQ    : EQUALS,
    token.LT        : LESSGREATER,
    token.GT        : LESSGREATER,
    token.PLUS      : SUM,
    token.MINUS     : SUM,
    token.SLASH     : PRODUCT,
    token.ASTERISK  : PRODUCT,
    token.LPAREN    : CALL,
}