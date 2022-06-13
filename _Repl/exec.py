import os
import _Lexer.lexer as lexer
import _Parser.parser as parser
import _Object.object as object
import _Evaluator.evaluator as evaluator

def start(path : str):
    filePath = os.getcwd() + "/" + str(path)
    print(filePath)
    if not os.path.exists(filePath):
        print("File not found!")
        return
    
    with open(filePath, 'r', encoding="ASCII") as f:
        lines = f.read()
        env = object.Environment()

        l = lexer.Lexer(lines)   
        p = parser.Parser(l)

        program = p.parseProgram()
        if len(p.getErrors()) != 0:
            printParserErrors(p.getErrors())
    
        evaluated = evaluator.Eval(program, env)
        if evaluated is not None:
            print(evaluated.inspect())

def printParserErrors(errors):
    for msg in errors:
        print("\t" + msg)