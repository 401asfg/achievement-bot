import unittest
from typing import List

from command.exceptions import ParsingError
from command.expression import StringExpr, NumberExpr, DirectionExpr, HelpCmdExpr, CharacterCmdExpr, MoveCmdExpr, \
    Expression
from command.keyword_lib import COMMAND_HELP, COMMAND_CHARACTER
from command.parser import parse
from command.token import Token, TokenType


class TestParser(unittest.TestCase):
    token_help: Token = Token(TokenType.COMMAND, COMMAND_HELP)

    token_character: Token = Token(TokenType.COMMAND, COMMAND_CHARACTER)
    token_word_one: Token = Token(TokenType.WORD, "Michael")
    token_word_two: Token = Token(TokenType.WORD, "Brian")
    token_end_word: Token = Token(TokenType.END_WORD, "Allan")

    token_move: Token = Token(TokenType.COMMAND, "move")
    token_direction: Token = Token(TokenType.DIRECTION, "right")
    token_number: Token = Token(TokenType.NUMBER, "11")

    tokens_help: List[Token]
    tokens_character: List[Token]
    tokens_move: List[Token]

    def setUp(self) -> None:
        self.tokens_help = [self.token_help]
        self.tokens_character = [self.token_character,
                                 self.token_word_one,
                                 self.token_word_two,
                                 self.token_end_word]
        self.tokens_move = [self.token_move,
                            self.token_direction,
                            self.token_number]

    def test_parse(self):
        def assert_correct(tokens: List[Token], expected_expr: Expression):
            actual_expr = parse(tokens)
            self.assertEqual(expected_expr, actual_expr)

        def assert_fail(tokens: List[Token]):
            try:
                parse(tokens)
                self.fail()
            except ParsingError:
                pass

        assert_correct(self.tokens_help,
                       HelpCmdExpr(self.token_help.value))

        assert_correct(self.tokens_character,
                       CharacterCmdExpr(self.token_character.value,
                                        StringExpr(self.token_word_one.value,
                                                   StringExpr(self.token_word_two.value,
                                                              StringExpr(self.token_end_word.value,
                                                                         None)))))

        assert_correct([self.token_character,
                        self.token_word_two,
                        self.token_word_one],
                       CharacterCmdExpr(self.token_character.value,
                                        StringExpr(self.token_word_two.value,
                                                   StringExpr(self.token_word_one.value,
                                                              None))))

        assert_correct([self.token_character,
                        self.token_word_one,
                        self.token_word_two,
                        self.token_word_one,
                        self.token_end_word],
                       CharacterCmdExpr(self.token_character.value,
                                        StringExpr(self.token_word_one.value,
                                                   StringExpr(self.token_word_two.value,
                                                              StringExpr(self.token_word_one.value,
                                                                         StringExpr(self.token_end_word.value,
                                                                                    None))))))

        assert_correct([self.token_character,
                        self.token_word_one,
                        self.token_word_one,
                        self.token_end_word],
                       CharacterCmdExpr(self.token_character.value,
                                        StringExpr(self.token_word_one.value,
                                                   StringExpr(self.token_word_one.value,
                                                              StringExpr(self.token_end_word.value,
                                                                         None)))))

        assert_correct([self.token_character,
                        self.token_word_one],
                       CharacterCmdExpr(self.token_character.value,
                                        StringExpr(self.token_word_one.value,
                                                   None)))

        assert_correct([self.token_character,
                        self.token_end_word],
                       CharacterCmdExpr(self.token_character.value,
                                        StringExpr(self.token_end_word.value,
                                                   None)))

        assert_correct(self.tokens_move,
                       MoveCmdExpr(self.token_move.value,
                                   DirectionExpr(self.token_direction.value),
                                   NumberExpr(self.token_number.value)))

        assert_correct([self.token_move,
                        self.token_direction],
                       MoveCmdExpr(self.token_move.value,
                                   DirectionExpr(self.token_direction.value),
                                   NumberExpr("1")))

        assert_fail([self.token_character,
                     self.token_number])

        assert_fail([self.token_character])

        assert_fail([self.token_help,
                     self.token_number])

        assert_fail([self.token_move,
                     self.token_direction,
                     self.token_number,
                     self.token_number])

        assert_fail([self.token_character,
                     self.token_end_word,
                     self.token_word_one])

        assert_fail([self.token_number])

        assert_fail([self.token_word_one,
                     self.token_end_word])

        assert_fail([self.token_move,
                     self.token_number,
                     self.token_number])

        assert_fail([self.token_move,
                     self.token_number,
                     self.token_direction])

        assert_fail([self.token_move,
                     self.token_end_word,
                     self.token_direction])

        assert_fail([self.token_move,
                     self.token_number,
                     self.token_end_word])

        assert_fail([self.token_move])

        assert_fail([])


if __name__ == '__main__':
    unittest.main()
