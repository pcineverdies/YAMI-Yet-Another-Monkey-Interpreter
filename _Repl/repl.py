import _Lexer.lexer as lexer
import _Parser.parser as parser
import _Object.object as object
import _Evaluator.evaluator as evaluator

PROMPT = ">> "

def start():

    env = object.Environment()

    while True:
        line = input(PROMPT)
        l = lexer.Lexer(line)   
        p = parser.Parser(l)

        program = p.parseProgram()
        if len(p.getErrors()) != 0:
            printParserErrors(p.getErrors())
        
        evaluated = evaluator.Eval(program, env)
        if evaluated is not None:
            print(evaluated.inspect())
            if evaluated.type() == object.EXIT_OBJ:
                return


def printParserErrors(errors):
    for msg in errors:
        print("\t" + msg)


