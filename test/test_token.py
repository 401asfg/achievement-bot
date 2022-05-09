import unittest
from typing import Tuple

from command.token import Token, TokenType, TOKEN_TYPE_OF_KEYWORD_DICT


class TestToken(unittest.TestCase):
    def test_init(self):
        def assert_init(type: TokenType, value: str):
            token = Token(type, value)
            self.assertEqual(token.type, type)
            self.assertEqual(token.value, value)

        assert_init(TokenType.COMMAND, "command")
        assert_init(TokenType.DIRECTION, "direction")
        assert_init(TokenType.NUMBER, "number")
        assert_init(TokenType.WORD, "string")


if __name__ == '__main__':
    unittest.main()
