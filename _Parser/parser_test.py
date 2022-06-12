from dataclasses import dataclass
from _Lexer.lexer import *
from _Ast.ast import *
from _Parser.parser import *
import unittest
import string

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
        self.checkEqualValue("stt.name", stt.name.tokenLiteral(), expectedIdentifier)
    
    def checkParserErrors(self, parser):
        errors = parser.getErrors()   
        msgError = "\npaser has {} errors".format(len(errors))

        for msg in errors:
            msgError = msgError + "\nparser error: {}".format(msg)

        self.assertEqual(len(errors), 0, msgError)
    
    def testReturnStatements(self):
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
        
    def testIdentifierExpression(self):
        input = "foobar"

        l = Lexer(input)
        p = Parser(l)

        program = p.parseProgram()
        self.checkParserErrors(p)

        self.checkLen(program.statements, 1)
        stmt = program.statements[0]
        self.checkInstanceOf(stmt, ExpressionStatement)
        ident = stmt.expression
        self.checkEqualValue("ident.value", ident.value, "foobar")
        self.checkEqualValue("ident.tokenLiteral", ident.tokenLiteral(), "foobar")

    def testIntegerLiteralExpression(self):
        input = "5;"
        l = Lexer(input)
        p = Parser(l)

        program = p.parseProgram()
        self.checkParserErrors(p)

        self.checkLen(program.statements, 1)
        stmt = program.statements[0]
        self.checkInstanceOf(stmt, ast.ExpressionStatement)
        
        literal = stmt.expression
        self.checkInstanceOf(literal, ast.IntegerLiteral)
        self.checkEqualValue("literal.value", literal.value, 5)
        self.checkEqualValue("literal.tokenLiteral", literal.tokenLiteral(), "5")
    
    def testParsingPrefixExpression(self):

        @dataclass
        class TestCase:
            input:          string
            operator:       string
            integerValue:   int
        
        prefixTest = [
            TestCase("!5", "!", 5),
            TestCase("-15", "-", 15)
        ]

        for elem in prefixTest:
            l = Lexer(elem.input)
            p = Parser(l)

            program = p.parseProgram()
            self.checkParserErrors(p)

            self.checkLen(program.statements, 1)
            stmt = program.statements[0]
            self.checkInstanceOf(stmt, ExpressionStatement)
            exp = stmt.expression
            self.checkInstanceOf(exp, PrefixExpression)
            self.checkEqualValue("exp.operator", exp.operator, elem.operator)
            self.integerLiteral(exp.right, elem.integerValue)
        
    def integerLiteral(self, il, value):
        self.checkInstanceOf(il, IntegerLiteral)
        self.checkEqualValue("il.value", il.value, value)
        self.checkEqualValue("il.tokenLiteral", il.tokenLiteral(), str(value))


    def testParsingInfixExpression(self):
        @dataclass
        class TestCase:
            input:      string
            leftValue:  int
            operator:   string
            rightValue: int
        
        infixTests = [
            TestCase("5 + 5;",  5, "+",  5), 
            TestCase("5 - 5;",  5, "-",  5), 
            TestCase("5 * 5;",  5, "*",  5), 
            TestCase("5 / 5;",  5, "/",  5),
            TestCase("5 > 5;",  5, ">",  5), 
            TestCase("5 < 5;",  5, "<",  5), 
            TestCase("5 == 5;", 5, "==", 5), 
            TestCase("5 != 5;", 5, "!=", 5),
        ]

        for elem in infixTests:
            l = Lexer(elem.input)
            p = Parser(l)

            program = p.parseProgram()
            self.checkParserErrors(p)

            self.checkLen(program.statements, 1)
            stmt = program.statements[0]
            self.checkInstanceOf(stmt, ExpressionStatement)
            exp = stmt.expression
            self.checkInstanceOf(exp, InfixExpression)
            self.integerLiteral(exp.left, elem.leftValue)
            self.checkEqualValue("exp.operator", exp.operator, elem.operator)
            self.integerLiteral(exp.right, elem.rightValue)

    def testOperatorPrecedenceParsing(self):
        @dataclass
        class TestCase:
            input:      string
            expected:   string
        
        tests = [
            TestCase("!-a", "(!(-a))",                                                     ),
            TestCase("a + b + c", "((a + b) + c)",                                         ),
            TestCase("a + b - c","((a + b) - c)",                                          ),
            TestCase("a * b * c","((a * b) * c)",                                          ),
            TestCase("a * b / c","((a * b) / c)",                                          ),
            TestCase("a + b / c","(a + (b / c))",                                          ),
            TestCase("a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"            ), 
            TestCase("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
        ]

        for elem in tests:
            l = Lexer(elem.input)
            p = Parser(l)

            program = p.parseProgram()
            self.checkParserErrors(p)

            actual = program.string()
            self.checkEqualValue("parsed", elem.expected, actual)

    def checkLen(self, stmts, expectedLen):
        self.assertTrue(len(stmts) == expectedLen, 
            "program.statements does not contain {} statemets. Got {}".format(expectedLen, len(stmts)))   
    def checkTokenLiteral(self, token, expected):
        self.assertEqual(token, expected, 
            "stt.TokenLiteral not '{}'. Got {}".format(expected,token))
    def checkInstanceOf(self, stt, className):    
        self.assertTrue(isinstance(stt, className),
                "stt not an instance of {}. Got {}".format(className.__name__, stt.__class__.__name__))
    def checkEqualValue(self, arg, value, expected):
        self.assertEqual(value, expected, 
            "{} not {}. Got {}".format(arg, expected, value))