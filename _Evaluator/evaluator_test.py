from dataclasses import dataclass
import unittest
import _Lexer.lexer as lexer
import _Parser.parser as parser
import _Object.object as object
import _Evaluator.evaluator as evaluator

class TestEvaluator(unittest.TestCase):
    def testEvalInteger(self):
        @dataclass
        class TestCase:
            input       : str
            expected    : int
        
        tests = [ 
            TestCase("5", 5),
            TestCase("10", 10),
            TestCase("-5", -5),
            TestCase("-10", -10),
            TestCase("5 + 5 + 5 + 5 - 10", 10),
            TestCase("2 * 2 * 2 * 2 * 2", 32),
            TestCase("-50 + 100 + -50", 0),
            TestCase("5 * 2 + 10", 20),
            TestCase("5 + 2 * 10", 25),
            TestCase("20 + 2 * -10", 0),
            TestCase("50 / 2 * 2 + 10", 60),
            TestCase("2 * (5 + 10)", 30),
            TestCase("3 * 3 * 3 + 10", 37),
            TestCase("3 * (3 * 3) + 10", 37),
            TestCase("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
        ]

        for elem in tests: 
            evaluated = self.eval(elem.input)
            self.typeObject(evaluated, elem.expected, object.Integer)

    def testEvalBooleanExpression(self):
        @dataclass
        class TestCase:
            input       : str
            expected    : bool
        
        tests = [ 
            TestCase("true", True),
            TestCase("false", False),
            TestCase("1 < 2", True),
            TestCase("1 > 2", False),
            TestCase("1 < 1", False),
            TestCase("1 > 1", False),
            TestCase("1 == 1", True),
            TestCase("1 != 1", False),
            TestCase("1 == 2", False),
            TestCase("1 != 2", True),
            TestCase("true == true", True),
            TestCase("false == false", True),
            TestCase("true == false", False),
            TestCase("true != false", True),
            TestCase("false != true", True),
            TestCase("(1 < 2) == true", True),
            TestCase("(1 < 2) == false", False),
            TestCase("(1 > 2) == true", False),
            TestCase("(1 > 2) == false", True),
        ]

        for elem in tests: 
            evaluated = self.eval(elem.input)
            self.typeObject(evaluated, elem.expected, object.Boolean)
        
    def eval(self, input : str) -> object.Object:
        l = lexer.Lexer(input)
        p = parser.Parser(l)
        program = p.parseProgram()

        return evaluator.Eval(program)
    
    def typeObject(self, obj : object.Object, expected : any, typeObject : any):
        self.checkInstanceOf(obj, typeObject)
        self.checkValue(obj.value, expected)

    def testBangOperator(self):
        @dataclass
        class TestCase:
            input : str
            expected : bool
        
        tests = [ 
            TestCase("!true", False),
            TestCase("!false", True),
            TestCase("!5", False),
            TestCase("!!true", True),
            TestCase("!!false", False),
            TestCase("!!5", True),
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            self.typeObject(evaluated, elem.expected, object.Boolean)

    def testIfElseExpressions(self):
        @dataclass
        class TestCase:
            input : str
            expected : any
        
        tests = [ 
            TestCase("if (true) ( 10 )", 10),
            TestCase("if (false) ( 10 )", None),
            TestCase("if (1) ( 10 )", 10),
            TestCase("if (1 < 2) ( 10 )", 10),
            TestCase("if (1 > 2) ( 10 )", None),
            TestCase("if (1 > 2) ( 10 ) else ( 20 )", 20),
            TestCase("if (1 < 2) ( 10 ) else ( 20 )", 10),
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            if isinstance(elem.expected, int):
                self.typeObject(evaluated, int(elem.expected), object.Integer)
            else:
                self.nullObject(evaluated)
            
    def nullObject(self, evaluated : object.Object):
        self.assertEqual(evaluated, object.NULL, "object is not NULL")

    def checkInstanceOf(self, stt, className):    
        self.assertTrue(isinstance(stt, className),
                "stt not an instance of {}. Got {}".format(className.__name__, stt.__class__.__name__))
    def checkValue(self, got : any, wanted : any):
        self.assertEqual(got, wanted,
                "object has wrong value. got={}, want={}".format(got, wanted))
