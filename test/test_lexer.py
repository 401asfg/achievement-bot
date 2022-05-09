import unittest
from typing import List

from command.exceptions import LexError
from command.keyword_lib import COMMAND_HELP, COMMAND_CHARACTER, COMMAND_MOVE, DIRECTION_RIGHT, COMMAND_INDICATOR, \
    STRING_WRAPPER
from command.lexer import lex
from command.token import Token, TokenType


class TestLexer(unittest.TestCase):
    def test_lex(self):
        def assert_correct(message: str, expected_tokens: List[Token]):
            actual_tokens = lex(message)
            self.assertEqual(expected_tokens, actual_tokens)

        def assert_fail(message: str):
            try:
                lex(message)
                self.fail()
            except LexError:
                pass

        assert_correct(COMMAND_INDICATOR + COMMAND_HELP,
                       [Token(TokenType.COMMAND, COMMAND_HELP)])

        assert_correct(COMMAND_INDICATOR + COMMAND_CHARACTER + " " + STRING_WRAPPER + "name" + STRING_WRAPPER,
                       [Token(TokenType.COMMAND, COMMAND_CHARACTER),
                        Token(TokenType.END_WORD, "name")])

        assert_correct(COMMAND_INDICATOR + COMMAND_CHARACTER + " " + STRING_WRAPPER + "name 2" + STRING_WRAPPER,
                       [Token(TokenType.COMMAND, COMMAND_CHARACTER),
                        Token(TokenType.WORD, "name"),
                        Token(TokenType.END_WORD, "2")])

        assert_correct(COMMAND_INDICATOR + COMMAND_CHARACTER + " " + STRING_WRAPPER + "name 2",
                       [Token(TokenType.COMMAND, COMMAND_CHARACTER),
                        Token(TokenType.WORD, "name"),
                        Token(TokenType.WORD, "2")])

        assert_correct(COMMAND_INDICATOR + COMMAND_MOVE + " " + DIRECTION_RIGHT + " 23",
                       [Token(TokenType.COMMAND, COMMAND_MOVE),
                        Token(TokenType.DIRECTION, DIRECTION_RIGHT),
                        Token(TokenType.NUMBER, "23")])

        assert_correct(COMMAND_INDICATOR + COMMAND_CHARACTER + " " + STRING_WRAPPER + " james one " + STRING_WRAPPER +
                       " 34 " + COMMAND_MOVE,
                       [Token(TokenType.COMMAND, COMMAND_CHARACTER),
                        Token(TokenType.WORD, ""),
                        Token(TokenType.WORD, "james"),
                        Token(TokenType.WORD, "one"),
                        Token(TokenType.END_WORD, ""),
                        Token(TokenType.NUMBER, "34"),
                        Token(TokenType.COMMAND, COMMAND_MOVE)])

        assert_correct(COMMAND_INDICATOR + STRING_WRAPPER + COMMAND_MOVE + STRING_WRAPPER + " " + DIRECTION_RIGHT +
                       " 23",
                       [Token(TokenType.END_WORD, COMMAND_MOVE),
                        Token(TokenType.DIRECTION, DIRECTION_RIGHT),
                        Token(TokenType.NUMBER, "23")])

        assert_correct(COMMAND_INDICATOR + STRING_WRAPPER + COMMAND_MOVE + " " + DIRECTION_RIGHT +
                       " 23",
                       [Token(TokenType.WORD, COMMAND_MOVE),
                        Token(TokenType.WORD, DIRECTION_RIGHT),
                        Token(TokenType.WORD, "23")])

        assert_correct(COMMAND_INDICATOR + STRING_WRAPPER + COMMAND_MOVE + " " + DIRECTION_RIGHT +
                       " 23" + STRING_WRAPPER,
                       [Token(TokenType.WORD, COMMAND_MOVE),
                        Token(TokenType.WORD, DIRECTION_RIGHT),
                        Token(TokenType.END_WORD, "23")])

        assert_fail(COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + "invalid!!!!!!!!!!!!!!!!!!!!!!!!!!")
        assert_fail("invalid!!!!!!!!!!!!!!!!!!!")

        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER)
        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + STRING_WRAPPER + COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + STRING_WRAPPER + STRING_WRAPPER + COMMAND_HELP)

        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + " " + COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + " " + STRING_WRAPPER + COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + STRING_WRAPPER + " " + COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + STRING_WRAPPER + STRING_WRAPPER + " " +
                    COMMAND_HELP)

        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + STRING_WRAPPER + " " + STRING_WRAPPER +
                    COMMAND_HELP)

        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + " " + STRING_WRAPPER + STRING_WRAPPER +
                    COMMAND_HELP)

        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + COMMAND_HELP + STRING_WRAPPER + COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + STRING_WRAPPER + COMMAND_HELP + STRING_WRAPPER + COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + STRING_WRAPPER + COMMAND_HELP + " " + STRING_WRAPPER + COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + STRING_WRAPPER + COMMAND_HELP + STRING_WRAPPER + " " + COMMAND_HELP +
                    STRING_WRAPPER)

        assert_fail(COMMAND_INDICATOR + STRING_WRAPPER + COMMAND_HELP + STRING_WRAPPER + STRING_WRAPPER + COMMAND_HELP)
        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + COMMAND_HELP + STRING_WRAPPER)
        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + " " + COMMAND_HELP + STRING_WRAPPER)
        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + " " + STRING_WRAPPER + COMMAND_HELP +
                    STRING_WRAPPER)

        assert_fail(COMMAND_INDICATOR + COMMAND_HELP + STRING_WRAPPER + STRING_WRAPPER + COMMAND_HELP + STRING_WRAPPER)


if __name__ == '__main__':
    unittest.main()
