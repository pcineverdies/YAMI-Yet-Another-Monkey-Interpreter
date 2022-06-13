import _Lexer.lexer as lexer
import _Token.token as token
import _Parser.parser as parser
import _Evaluator.evaluator as evaluator

PROMPT = ">> "

def start():

    while True:
        line = input(PROMPT)

        l = lexer.Lexer(line)   
        p = parser.Parser(l)

        program = p.parseProgram()
        if len(p.getErrors()) != 0:
            printParserErrors(p.getErrors())
        
        evaluated = evaluator.Eval(program)
        if evaluated is not None:
            print(evaluated.insepct())

def printParserErrors(errors):
    for msg in errors:
        print("\t" + msg)


