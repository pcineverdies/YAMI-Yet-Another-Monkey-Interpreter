import _Lexer.lexer as lexer
import _Token.token as token

PROMPT = ">> "

def start():

    while True:
        line = input(PROMPT)

        l = lexer.Lexer(line)

        tok = l.nextToken()

        while tok.type != token.EOF:
            print(tok)
            tok = l.nextToken()


