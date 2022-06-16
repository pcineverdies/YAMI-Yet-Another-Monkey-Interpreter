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
        
            !-*/5;
            5 < 10 > 5;

            if (5 < 10) {
                return true;
            }
            else {
                return false;
            }

            10 == 10;
            10 != 9;
            "foobar"
            "foo bar"
            [1, 2];
            {"foo" : "bar"}
            4 <= 5 >= 5 || 5 && 5 and 5 or 5 % 5;

            while (a < 5){
                let a = a + 1;
                break;
                continue;
            }

            for(;;){

            }
            class
            classname.method
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
            newToken(ASTERISK,     "*"),
            newToken(SLASH,        "/"),
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
            newToken(STRING,       "foobar"),
            newToken(STRING,       "foo bar"),
            newToken(LBRACKET,     "["),
            newToken(INT,          "1"),
            newToken(COMMA,        ","),
            newToken(INT,          "2"),
            newToken(RBRACKET,     "]"),
            newToken(SEMICOLON,    ";"),
            newToken(LBRACE,       "{"),
            newToken(STRING,       "foo"),
            newToken(COLON,        ":"),
            newToken(STRING,       "bar"),
            newToken(RBRACE,       "}"),
            newToken(INT,          "4"),
            newToken(LTE,          "<="),
            newToken(INT,          "5"),
            newToken(GTE,          ">="),
            newToken(INT,          "5"),
            newToken(OR,           "||"),
            newToken(INT,          "5"),
            newToken(AND,          "&&"),
            newToken(INT,          "5"),
            newToken(AND,          "and"),
            newToken(INT,          "5"),
            newToken(OR,           "or"),
            newToken(INT,          "5"),
            newToken(MODULUS,      "%"),
            newToken(INT,          "5"),
            newToken(SEMICOLON,    ";"),
            newToken(WHILE,        "while"),
            newToken(LPAREN,       "("),
            newToken(IDENT,        "a"),
            newToken(LT,           "<"),
            newToken(INT,          "5"),
            newToken(RPAREN,       ")"),
            newToken(LBRACE,       "{"),
            newToken(LET,          "let"),
            newToken(IDENT,        "a"),
            newToken(ASSIGN,       "="),
            newToken(IDENT,        "a"),
            newToken(PLUS,         "+"),
            newToken(INT,          "1"),
            newToken(SEMICOLON,    ";"),
            newToken(BREAK,        "break"),
            newToken(SEMICOLON,    ";"),
            newToken(CONTINUE,     "continue"),
            newToken(SEMICOLON,    ";"),
            newToken(RBRACE,       "}"),
            newToken(FOR,          "for"),
            newToken(LPAREN,       "("),
            newToken(SEMICOLON,    ";"),
            newToken(SEMICOLON,    ";"),
            newToken(RPAREN,       ")"),
            newToken(LBRACE,       "{"),
            newToken(RBRACE,       "}"),
            newToken(CLASS,        "class"),
            newToken(IDENT,        "classname"),
            newToken(DOT,          "."),
            newToken(IDENT,        "method"),
            newToken(EOF,          "")
        ]

        l = Lexer(input)

        for item in expected:
            tok = l.nextToken()
            self.assertEqual(item.type, tok.type, "expected {}, got {}".format(item.type, tok.type))
            self.assertEqual(item.literal, tok.literal, "expected {}, got {}".format(item.literal, tok.literal))
