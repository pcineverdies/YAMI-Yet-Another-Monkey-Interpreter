import array
from dataclasses import dataclass
from turtle import st
from _Lexer.lexer import *
from _Ast.ast import *
from _Parser.parser import *
import unittest
import string

class TestParser(unittest.TestCase):
    def testLetStatements(self):
        @dataclass
        class TestCase:
            input :              str
            expectedIdentifier : str
            expectedValue :      ...

        tests = [
            TestCase("let x = 5", "x", 5),
            TestCase("let y = true", "y", True),
            TestCase("let foobar = y", "foobar", "y"),
        ] 

        for elem in tests:
            l = Lexer(elem.input)
            p = Parser(l)        

            program = p.parseProgram()
            self.checkParserErrors(p)

            self.checkLen(program.statements, 1)

            stmt = program.statements[0]
            self.letStatement(stmt, elem.expectedIdentifier)
            val = stmt.value
            self.literalExpression(val, elem.expectedValue)

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
            value:          Expression
        
        prefixTest = [
            TestCase("!5", "!", 5),
            TestCase("-15", "-", 15),
            TestCase("!false", "!", False),
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
            self.literalExpression(exp.right, elem.value)
        
    def integerLiteral(self, il, value):
        self.checkInstanceOf(il, IntegerLiteral)
        self.checkEqualValue("il.value", il.value, value)
        self.checkEqualValue("il.tokenLiteral", il.tokenLiteral(), str(value))

    def infixExpression(self, exp, left, operator, right):
        self.checkInstanceOf(exp, InfixExpression)
        self.literalExpression(exp.left, left)
        self.checkEqualValue("exp.operator", operator, exp.operator)
        self.literalExpression(exp.right, right)

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
            TestCase("true != false", True, "!=", False),
        ]

        for elem in infixTests:
            l = Lexer(elem.input)
            p = Parser(l)

            program = p.parseProgram()
            self.checkParserErrors(p)

            self.checkLen(program.statements, 1)
            self.checkInstanceOf(program.statements[0], ExpressionStatement)
            exp = program.statements[0].expression
            self.infixExpression(exp, elem.leftValue, elem.operator, elem.rightValue)

    def testOperatorPrecedenceParsing(self):
        @dataclass
        class TestCase:
            input:      string
            expected:   string
        
        tests = [
            TestCase("!-a", "(!(-a))",                                  ),
            TestCase("a + b + c", "((a + b) + c)",                      ),
            TestCase("a + b - c","((a + b) - c)",                       ),
            TestCase("a * b * c","((a * b) * c)",                       ),
            TestCase("a * b / c","((a * b) / c)",                       ),
            TestCase("a + b / c","(a + (b / c))",                       ),
            TestCase("a + b * c + d / e - f", 
                     "(((a + (b * c)) + (d / e)) - f)"                  ), 
            TestCase("3 + 4 * 5 == 3 * 1 + 4 * 5", 
                     "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"           ),
            TestCase("3 < 5 == false", "((3 < 5) == false)"             ),
            TestCase("3 < 5 == false", "((3 < 5) == false)"             ),
            TestCase("3 < 5 == false", "((3 < 5) == false)"             ),
            TestCase("( 5 + 5 ) * 2", "((5 + 5) * 2)"                   ),
            TestCase("-( 5 + 5 )", "(-(5 + 5))"                         ),
            TestCase("!(true == false)", "(!(true == false))"           ),
            TestCase("a + add(b * c) + d", "((a + add((b * c))) + d)"   ),
            TestCase("add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))", 
                     "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))"  ),
            TestCase("!(true == false)", "(!(true == false))"           ),

        ]

        for elem in tests:
            l = Lexer(elem.input)
            p = Parser(l)

            program = p.parseProgram()
            self.checkParserErrors(p)

            actual = program.string()
            self.checkEqualValue("parsed", elem.expected, actual)

    def identifier(self, exp, value):
        self.checkInstanceOf(exp, Identifier)
        self.checkEqualValue("exp.value", value, exp.value)
        self.checkEqualValue("exp.tokenLiteral", value, exp.tokenLiteral())

    def literalExpression(self, exp, expected):
        if isinstance(expected, bool):
            self.boolean(exp, expected)
        elif isinstance(expected, int):
            self.integerLiteral(exp, int(expected))
        elif isinstance(expected, str):
            self.identifier(exp, expected)
        else:
            self.fail("type of exp not handled. got={}", exp)

    def boolean(self, exp, value):
        self.checkInstanceOf(exp, Boolean)
        self.checkEqualValue("exp.value", value, exp.value)
        value = "true" if value else "false"
        self.checkEqualValue("exp.tokenLiteral", value, exp.tokenLiteral())

    def testBooleanExpression(self):
        @dataclass
        class TestCase:
            input:      string
            expected:   bool
        
        tests = [
            TestCase("true", True),
            TestCase("false", False),
        ]

        for elem in tests:
            l = Lexer(elem.input)
            p = Parser(l)

            program = p.parseProgram()
            self.checkParserErrors(p)

            self.checkLen(program.statements, 1)
            self.checkInstanceOf(program.statements[0], ExpressionStatement)
            exp = program.statements[0].expression
            self.literalExpression(exp, elem.expected)
    
    def testIfExpression(self):
        input = "if (x < y) { x }"
        l = Lexer(input)
        p = Parser(l)

        program = p.parseProgram()
        self.checkParserErrors(p)
    
        self.checkLen(program.statements, 1)
        stmt = program.statements[0]
        self.checkInstanceOf(stmt, ExpressionStatement)
        exp = stmt.expression
        self.checkInstanceOf(exp, IfExpression)
        self.infixExpression(exp.condition, "x", "<", "y")
        self.checkLen(exp.consequence.statements, 1)
        consequence = exp.consequence.statements[0]
        self.checkInstanceOf(consequence, ExpressionStatement)
        self.identifier(consequence.expression, "x")
        self.checkEqualValue("exp.alternative.statements", exp.alternative, None)

    def testIfElseExpression(self):
        input = "if (x < y) { x } else { y }"
        l = Lexer(input)
        p = Parser(l)

        program = p.parseProgram()
        self.checkParserErrors(p)
    
        self.checkLen(program.statements, 1)
        stmt = program.statements[0]
        self.checkInstanceOf(stmt, ExpressionStatement)
        exp = stmt.expression
        self.checkInstanceOf(exp, IfExpression)
        self.infixExpression(exp.condition, "x", "<", "y")
        self.checkLen(exp.consequence.statements, 1)
        consequence = exp.consequence.statements[0]
        self.checkInstanceOf(consequence, ExpressionStatement)
        self.identifier(consequence.expression, "x")

        self.checkLen(exp.alternative.statements, 1)
        alternative = exp.alternative.statements[0]
        self.checkInstanceOf(alternative, ExpressionStatement)
        self.identifier(alternative.expression, "y")

    def testFunctionLiteralParsing(self):
        input = "fn(x, y) { x + y }"

        l = Lexer(input)
        p = Parser(l)

        program = p.parseProgram()
        self.checkParserErrors(p)

        self.checkLen(program.statements, 1)
        stmt = program.statements[0]
        self.checkInstanceOf(stmt, ExpressionStatement)
        function = stmt.expression
        self.checkInstanceOf(function, FunctionLiteral)
        self.checkLen(function.parameters, 2)
        self.literalExpression(function.parameters[0], "x")
        self.literalExpression(function.parameters[1], "y")
        self.checkLen(function.body.statements, 1)
        bodystmt = function.body.statements[0]
        self.checkInstanceOf(bodystmt, ExpressionStatement)
        self.infixExpression(bodystmt.expression, "x", "+", "y")
    
    def testFunctionParameterParsing(self):
        @dataclass
        class TestCase:
            input:                  str
            expectedParameters:     array

        tests = [
            TestCase("fn() {}", []),
            TestCase("fn(x) {}", ["x"]),
            TestCase("fn(x, y, z) {}", ["x", "y", "z"]),
        ]

        for elem in tests:
            l = Lexer(elem.input)
            p = Parser(l)

            program = p.parseProgram()
            self.checkParserErrors(p)

            stmt = program.statements[0]
            function = stmt.expression

            self.checkEqualValue("length parameters", len(function.parameters), len(elem.expectedParameters))
            for i, ident in enumerate(elem.expectedParameters):
                self.literalExpression(function.parameters[i], ident)

    def testCallExpressionParsing(self):
        input = "add(1, 2 * 3, 4 + 5)"

        l = Lexer(input)
        p = Parser(l)
        program = p.parseProgram()
        self.checkParserErrors(p)

        self.checkLen(program.statements, 1)
        stmt = program.statements[0]
        self.checkInstanceOf(stmt, ExpressionStatement)
        exp = stmt.expression
        self.checkInstanceOf(exp, CallExpression)
        self.identifier(exp.function, "add")
        self.checkLen(exp.arguments, 3)

        self.literalExpression(exp.arguments[0], 1)
        self.infixExpression(exp.arguments[1], 2, "*", 3)
        self.infixExpression(exp.arguments[2], 4, "+", 5)


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