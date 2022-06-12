from _Token.token import *
from _Lexer.lexer import *
import unittest

class TestToken(unittest.TestCase):
    def test_tokenizer(self):
        input = """
            let five = 5;
            let ten  = 10;

            let add  = fn(n, y) {
                x + y;
            };

            let result = add(five, ten);
        
            !-/*5;
            5 < 10 > 5;

            if (5 < 10) {
                return true;
            }
            else {
                return false;
            }

            10 == 10;
            10 != 9;
        """

        expected = [
            newToken(LET,          "let"),
            newToken(IDENT,        "five"),
            newToken(ASSIGN,       "="),
            newToken(INT,          "5"),
            newToken(SEMICOLON,    ";"),
            newToken(LET,          "let"),
            newToken(IDENT,        "ten"),
            newToken(ASSIGN,       "="),
            newToken(INT,          "10"),
            newToken(SEMICOLON,    ";"),
            newToken(LET,          "let"),
            newToken(IDENT,        "add"),
            newToken(ASSIGN,       "="),
            newToken(FUNCTION,     "fn"),
            newToken(LPAREN,       "("),
            newToken(IDENT,        "n"),
            newToken(COMMA,        ","),
            newToken(IDENT,        "y"),
            newToken(RPAREN,       ")"),
            newToken(LBRACE,       "{"),
            newToken(IDENT,        "x"),
            newToken(PLUS,         "+"),
            newToken(IDENT,        "y"),
            newToken(SEMICOLON,    ";"),
            newToken(RBRACE,       "}"),
            newToken(SEMICOLON,    ";"),
            newToken(LET,          "let"),
            newToken(IDENT,        "result"),
            newToken(ASSIGN,       "="),
            newToken(IDENT,        "add"),
            newToken(LPAREN,       "("),
            newToken(IDENT,        "five"),
            newToken(COMMA,        ","),
            newToken(IDENT,        "ten"),
            newToken(RPAREN,       ")"),
            newToken(SEMICOLON,    ";"),
            newToken(BANG,         "!"),
            newToken(MINUS,        "-"),
            newToken(SLASH,        "/"),
            newToken(ASTERISK,     "*"),
            newToken(INT,          "5"),
            newToken(SEMICOLON,    ";"),
            newToken(INT,          "5"),
            newToken(LT,           "<"),
            newToken(INT,          "10"),
            newToken(GT,           ">"),
            newToken(INT,          "5"),
            newToken(SEMICOLON,    ";"),
            newToken(IF,           "if"),
            newToken(LPAREN,       "("),
            newToken(INT,          "5"),
            newToken(LT,           "<"),
            newToken(INT,          "10"),
            newToken(RPAREN,       ")"),
            newToken(LBRACE,       "{"),
            newToken(RETURN,       "return"),
            newToken(TRUE,         "true"),
            newToken(SEMICOLON,    ";"),
            newToken(RBRACE,       "}"),
            newToken(ELSE,         "else"),
            newToken(LBRACE,       "{"),
            newToken(RETURN,       "return"),
            newToken(FALSE,        "false"),
            newToken(SEMICOLON,    ";"),
            newToken(RBRACE,       "}"),
            newToken(INT,          "10"),
            newToken(EQ,           "=="),
            newToken(INT,          "10"),
            newToken(SEMICOLON,    ";"),
            newToken(INT,          "10"),
            newToken(NOT_EQ,       "!="),
            newToken(INT,          "9"),
            newToken(SEMICOLON,    ";"),
            newToken(EOF,           "")
        ]

        l = Lexer(input)

        for item in expected:
            tok = l.nextToken()
            self.assertEqual(item.type, tok.type)
            self.assertEqual(item.literal, tok.literal)
