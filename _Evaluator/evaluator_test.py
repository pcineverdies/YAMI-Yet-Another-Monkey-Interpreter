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
        env = object.Environment()

        return evaluator.Eval(program, env)
    
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
            TestCase("if (true)     { 10 }", 10),
            TestCase("if (false)    { 10 }", None),
            TestCase("if (1)        { 10 }", 10),
            TestCase("if (1 < 2)    { 10 }", 10),
            TestCase("if (1 > 2)    { 10 }", None),
            TestCase("if (1 > 2)    { 10 } else { 20 }", 20),
            TestCase("if (1 < 2)    { 10 } else { 20 }", 10),
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            if isinstance(elem.expected, int):
                self.typeObject(evaluated, elem.expected, object.Integer)
            else:
                self.nullObject(evaluated)
        
    def testReturnStatements(self):
        @dataclass
        class TestCase:
            input : str
            expected : int
        
        tests = [
            TestCase("return 10;", 10),
            TestCase("return 10; 9", 10),
            TestCase("return 2 * 9; 4", 18),
            TestCase("9; return 2 * 4; 9", 8),
            TestCase("if (10 > 1) { if (10 > 1) { return 10; } return 1; }", 10)
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            self.typeObject(evaluated, elem.expected, object.Integer)

    def testErrorHandling(self):
        @dataclass
        class TestCase:
            input : str
            expectedMessage : str
        
        tests = [ 
            TestCase("5 + true;", "type mismatch: INTEGER + BOOLEAN"),
            TestCase("5 + true; 5", "type mismatch: INTEGER + BOOLEAN"),
            TestCase("-true", "unknown operator: -BOOLEAN"),
            TestCase("false + true;", "unknown operator: BOOLEAN + BOOLEAN"),
            TestCase("5; false + true; 5", "unknown operator: BOOLEAN + BOOLEAN"),
            TestCase("if (10 > 1) { true + false; }", "unknown operator: BOOLEAN + BOOLEAN"),
            TestCase("foobar", "identifier not found: foobar")
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            if not isinstance(evaluated, object.Error):
                self.fail("no error object returned")
            if evaluated.message != elem.expectedMessage:
                self.fail("wrong error message. expected {}, got {}".format( 
                           elem.expectedMessage, evaluated.message))
            
    def testLetStatements(self):
        @dataclass
        class TestCase:
            input : str
            expected : int
        
        tests = [ 
            TestCase("let a = 5; a;", 5),
            TestCase("let a = 5 * 5; a;", 25),
            TestCase("let a = 5; let b = a; b;", 5),
            TestCase("let a = 5; let b = a; let c = a + b + 5; c;", 15),
        ]

        for elem in tests:
            self.typeObject(self.eval(elem.input), elem.expected, object.Integer)
    
    def testFunctionObject(self):
        input = "fn(x) { x + 2 }"

        evaluated = self.eval(input)
        self.checkInstanceOf(evaluated, object.Function)
        self.assertEqual(len(evaluated.parameters), 1,
            "function has wrong paramters. got={}".format(len(evaluated.parameters)))
        self.assertEqual(evaluated.parameters[0].string(), "x",
            "parameters is not 'x'. got={}".format(evaluated.parameters[0].string()))
        
        expectBody = "{(x + 2);}"

        self.assertEqual(evaluated.body.string(), expectBody,
            "parameters is not {}. got={}".format(expectBody, evaluated.body.string()))

    def testFunctionApplication(self):
        @dataclass
        class TestCase:
            input : str
            expected : int
        
        tests = [ 
            TestCase("let identify = fn(x) {x;}; identify(5);", 5),
            TestCase("let identify = fn(x) {return x;}; identify(5);", 5),
            TestCase("let double = fn(x) {return x * 2;}; double(5);", 10),
            TestCase("let add = fn(x, y) {return x + y;}; add(5, 6);", 11),
            TestCase("let add = fn(x, y) {return x + y;}; add(5 + 5, add(5, 5));", 20),
            TestCase("fn(x){x;}(5)", 5)
        ]

        for elem in tests:
            self.typeObject(self.eval(elem.input), elem.expected, object.Integer)

    def nullObject(self, evaluated : object.Object):
        self.assertEqual(evaluated, object.NULL, "object is not NULL")

    def checkInstanceOf(self, stt, className):    
        self.assertTrue(isinstance(stt, className),
                "stt not an instance of {}. Got {}".format(className.__name__, stt.__class__.__name__))
    def checkValue(self, got : any, wanted : any):
        self.assertEqual(got, wanted,
                "object has wrong value. got={}, want={}".format(got, wanted))

    def testClosures(self):
        input = """
            let newAdder = fn(x) {
                fn(y) {x + y}
            };

            let addTwo = newAdder(2);
            addTwo(2);
        """

        self.typeObject(self.eval(input), 4, object.Integer)