import unittest
from _Token.token import *
from _Ast.ast import *

class TestAst(unittest.TestCase):
    def testString(self):
        p = Program()
        p.statements = [
            LetStatement(
                token = Token(
                    type = token.LET, 
                    literal = "let"
                ), 
                name  = Identifier(
                    token = Token(
                        type = token.IDENT, 
                        literal = "myVar"
                    ), 
                    value = "myVar"
                ),
                value = Identifier(
                    token = Token(
                        type = token.IDENT, 
                        literal = "anotherVar"
                    ), 
                    value = "anotherVar"
                ),
            ),
        ]

        self.assertEqual(p.string(), "let myVar = anotherVar;",
            "program.string() wrong. Got: {}".format(p.string()))