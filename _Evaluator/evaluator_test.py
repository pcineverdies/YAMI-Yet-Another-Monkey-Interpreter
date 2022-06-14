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
            TestCase("18 % 5", 3),
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
            TestCase("(4 <= 2) == true", False),
            TestCase("(1 <= 1) == true", True),
            TestCase("1 >= 18", False),
            TestCase("1 >= 1", True),
            TestCase("(1 < 2) == false", False),
            TestCase("(1 > 2) == true", False),
            TestCase("(1 > 2) == false", True),
            TestCase("(1 < 2) and false", False),
            TestCase("(1 < 2) and true", True)
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
            TestCase("if (10 > 1) { if (10 > 1) { return 10; } return 1; }", 10),
            TestCase("if (10 > 1) { if (10 > 1) { return; } return 1; }", 0),
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
            TestCase("foobar", "identifier not found: foobar"),
            TestCase('"A" - "B"', "unknown operator: STRING - STRING"),
            TestCase('{"name":"Monkey"}[fn(x){x}];', "unusable as hash key: FUNCTION"),
            TestCase('let a = 10; a = 20; b = 30;', "Can't assign value before declaration")
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            if not isinstance(evaluated, object.Error):
                self.fail("no error object returned")
            if evaluated.message != elem.expectedMessage:
                self.fail("wrong error message. expected `{}`, got `{}`".format( 
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
        
    def testStringLiteral(self):
        input = '"Hello World!"'

        evaluated = self.eval(input)
        self.checkInstanceOf(evaluated, object.String)
        self.checkValue(evaluated.value, "Hello World!")
    
    def testClosures(self):
        input = """
            let newAdder = fn(x) {
                fn(y) {x + y}
            };

            let addTwo = newAdder(2);
            addTwo(2);
        """
        self.typeObject(self.eval(input), 4, object.Integer)
    
    def testStringConcatenation(self):
        input = '"Hello" + " " +"World!"'

        evaluated = self.eval(input)
        self.checkInstanceOf(evaluated, object.String)
        self.checkValue(evaluated.value, "Hello World!")

    def testBuiltinFunctions(self):
        @dataclass
        class TestCase:
            input : str
            expected : any
        
        tests = [ 
            TestCase('len("");', 0),
            TestCase('len("four");', 4),
            TestCase('len("hello world");', 11),
            TestCase('len(1);', "argument to `len` not supported, got INTEGER"),
            TestCase('len("one", "two");', "wrong number of arguments. got=2, want=1"),
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)

            if isinstance(elem.expected, int):
                self.typeObject(evaluated, elem.expected, object.Integer)
            elif isinstance(elem.expected, str):
                if not isinstance(evaluated, object.Error):
                    self.fail("object is not error, got {}".format(evaluated.type()))
                self.checkValue(evaluated.message, elem.expected)

    def testArrayLiterals(self):
        input = "[1, 2 * 2, 3 + 3]"
        
        evaluated = self.eval(input)
        self.checkInstanceOf(evaluated, object.Array)
        self.assertEqual(len(evaluated.elements), 3,
            "array has wrong number of elements. got={}".format(len(evaluated.elements)))
        self.typeObject(evaluated.elements[0], 1, object.Integer)
        self.typeObject(evaluated.elements[1], 4, object.Integer)
        self.typeObject(evaluated.elements[2], 6, object.Integer)

    def testArrayIndexExpression(self):
        @dataclass
        class TestCase:
            input : str
            expected : any
        
        tests = [
		    TestCase("[1, 2, 3][0]", 1),
		    TestCase("[1, 2, 3][1]", 2),
		    TestCase("[1, 2, 3][2]", 3),
		    TestCase("let i = 0; [1][i];",1 ),
		    TestCase("[1, 2, 3][1 + 1];", 3),
		    TestCase("let myArray = [1, 2, 3]; myArray[2];", 3),
		    TestCase("let myArray = [1, 2, 3]; myArray[0] + myArray[1] + myArray[2];", 6),
		    TestCase("let myArray = [1, 2, 3]; let i = myArray[0]; myArray[i]", 2),
		    TestCase("[1, 2, 3][3]", None),
		    TestCase("[1, 2, 3][-1]", None),            
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            if isinstance(elem.expected, int):
                self.typeObject(evaluated, elem.expected, object.Integer)
            else:
                self.nullObject(evaluated)
            
    def testStringHashKey(self):
        t1 = object.String("Hello World")
        t2 = object.String("Hello World")
        t3 = object.String("foobar")
        t4 = object.String("foobar")
    
        self.assertEqual(t1.hashKey(), t2.hashKey(),    "strings with same content have different hash keys")
        self.assertEqual(t3.hashKey(), t4.hashKey(),    "strings with same content have different hash keys")
        self.assertNotEqual(t1.hashKey(), t3.hashKey(), "strings with different content have same hash keys")

    def testHashLiteral(self):
        input = """
            let two = "two";
            {
                "one" : 10 - 9,
                two   : 1 + 1,
                "thr" + "ee" : 6 / 2, 
                4 : 4,
                true : 5,
                false : 6
            }
        """

        evaluated = self.eval(input)
        self.checkInstanceOf(evaluated, object.Hash)

        expected = {
            object.String("one").hashKey()   : 1,
            object.String("two").hashKey()   : 2,
            object.String("three").hashKey() : 3,
            object.Integer(4).hashKey()      : 4,
            object.TRUE.hashKey()            : 5,
            object.FALSE.hashKey()           : 6,
        }

        self.assertEqual(len(evaluated.pairs), len(expected))

        for expectedKey, expectedValue in expected.items():
            if not expectedKey in evaluated.pairs:
                self.fail("no pair for given key in pairs")
            
        self.typeObject(evaluated.pairs[expectedKey].value, expectedValue, object.Integer)
    
    def testHashIndexExpression(self):
        @dataclass
        class TestCase:
            input : str
            expected : any
        
        tests = [ 
            TestCase('{"foo": 5}["foo"]', 5),
            TestCase('{"foo": 5}["bar"]', None),
            TestCase('let key = "foo"; {"foo": 5}[key]', 5),
            TestCase('{}["foo"]', None),
            TestCase('{5: 5}[5]', 5),
            TestCase('{true: 5}[true]', 5),
            TestCase('{false: 5}[false]', 5),
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            if isinstance(elem.expected, int):
                self.typeObject(evaluated, elem.expected, object.Integer)
            else:
                self.nullObject(evaluated)

    def testWhileExpression(self):
        @dataclass
        class TestCase:
            input : str
            expected : any
        
        tests = [ 
            TestCase("let a = 0; while (a < 10) { let a = a + 1; }; a;", 10),
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            if isinstance(elem.expected, int):
                self.typeObject(evaluated, elem.expected, object.Integer)
            else:
                self.nullObject(evaluated)
    
    def testAssignStatements(self):
        @dataclass
        class TestCase:
            input : str
            expected : int
        
        tests = [ 
            TestCase("let a = 5; a = 10; a;", 10),
            TestCase("let a = 5 * 5; a = 20; a;", 20),
            TestCase("let a = 5; let b = 10; b = a; b;", 5),
        ]

        for elem in tests:
            self.typeObject(self.eval(elem.input), elem.expected, object.Integer)

    def testBreakContinueStatements(self):
        @dataclass
        class TestCase:
            input : str
            expected : int
        
        tests = [ 
            TestCase("""
                let a = 5;
                let b = 10;
                while(true){
                    while(true) {
                        if (b == 20){
                            break;
                        }
                        else{
                            b = b + 1;
                        }
                    }
                    a = a + 1;
                    if (a == 10) {
                        break;
                    }
                }
                a+b; """, 30),
            TestCase("""
                let num = 0;
                let result = 0;

                while(num != 100) {
                    num = num + 1;
                    if(num % 2 == 1){
                        continue;
                    }
                    result = result + 1;
                }

                result;
            """, 50),
        ]

        for elem in tests:
            self.typeObject(self.eval(elem.input), elem.expected, object.Integer)

    def testForExpression(self):
        @dataclass
        class TestCase:
            input : str
            expected : any
        
        tests = [ 
            TestCase("""
                let result = 0;
                for(let i = 0; i < 10; i = i + 1){
                    result = result + i;
                }
                result;
            """, 45),
            TestCase("""
                let a = 30;
                for(;a < 40; a = a + 1){}
                a;
            """, 40),
            TestCase("""
                let a = 50;
                for(let a = 1;a < 40; a = a + 1){}
                a;
            """, 50),
        ]

        for elem in tests:
            evaluated = self.eval(elem.input)
            if isinstance(elem.expected, int):
                self.typeObject(evaluated, elem.expected, object.Integer)
            else:
                self.nullObject(evaluated)

# -------------------- NO TEST ----------------------------------

    def nullObject(self, evaluated : object.Object):
        self.assertEqual(evaluated, object.NULL, "object is not NULL")

    def checkInstanceOf(self, stt, className):    
        self.assertTrue(isinstance(stt, className),
                "stt not an instance of {}. Got {}".format(className.__name__, stt.__class__.__name__))
    def checkValue(self, got : any, wanted : any):
        self.assertEqual(got, wanted,
                "object has wrong value. got={}, want={}".format(got, wanted))
