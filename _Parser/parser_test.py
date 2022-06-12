from _Lexer.lexer import *
from _Ast.ast import *
from _Parser.parser import *
import unittest

class TestParser(unittest.TestCase):
    def testLetStatements(self):
        input = """
            let x = 5;
            let y = 10;
            let foobar = 838383;
        """

        l = Lexer(input)
        p = Parser(l)        

        program = p.parseProgram()
        self.checkParserErrors(p)

        self.checkLen(program.statements, 3)

        expected = ["x", "y", "foobar"]

        for i, tt in enumerate(expected):
            self.letStatement(program.statements[i], tt)

    def letStatement(self, stt, expectedIdentifier):
        self.checkTokenLiteral(stt.tokenLiteral(), "let")
        self.checkInstanceOf(stt, LetStatement)
        self.checkEqualValue("stt.name.vale", stt.name.value, expectedIdentifier)
        self.checkEqualValue("stt.name", stt.name.tokenLiteral, expectedIdentifier)
    
    def checkParserErrors(self, parser):
        errors = parser.getErrors()

        if len(errors) == 0:
            return
        
        msgError = "\npaser has {} errors".format(len(errors))
        for msg in errors:
            msgError = msgError + "\nparser error: {}".format(msg)
        
        self.fail(msgError)
    
    def testLetStatements(self):
        input = """
            return 4;
            return 10;
            return 24432;
        """

        l = Lexer(input)
        p = Parser(l)        

        program = p.parseProgram()
        self.checkParserErrors(p)

        self.checkLen(program.statements, 3)

        for stmt in program.statements:
            self.checkInstanceOf(stmt, ReturnStatement)
            self.checkTokenLiteral(stmt.tokenLiteral(), "return")
        
    def checkLen(self, stmts, expectedLen):
        self.assertTrue(len(stmts) == expectedLen, 
            "program.statements does not contain 3 statemets. Got {}".format(len(stmts)))
    
    def checkTokenLiteral(self, token, expected):
        self.assertEqual(token, expected, 
            "stt.TokenLiteral not '{}'. Got {}".format(expected,token))

    def checkInstanceOf(self, stt, className):    
        self.assertTrue(isinstance(stt, className),
                "stt not an instance of {}. Got {}".format(className.__name__, stt.__class__.__name__))

    def checkEqualValue(self, arg, value, expected):
        self.assertEqual(value, expected, 
            "{} not {}. Got {}".format(arg, expected, value))