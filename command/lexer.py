from dataclasses import dataclass
from enum import Enum
from typing import List

from command.exceptions import LexError
from command.keyword_lib import COMMAND_INDICATOR, STRING_WRAPPER
from command.token import TOKEN_TYPE_OF_KEYWORD_DICT, Token, TokenType


class Mode(Enum):
    """
    The possible modes of the lexer
    """
    NORMAL = 0
    STRING = 1


@dataclass
class State:
    """
    The current state of the lexer
    """
    mode: Mode


def _tokenize_string_start(lexeme: str, state: State) -> Token:
    """
    Produce a token for the start of a string

    :param lexeme: The first lexeme in a string
    :param state: The current state of the lexer
    :return: A token that represents the start of a string
    :raise LexError: If the given lexeme is not a valid start to a string
    """

    if lexeme.startswith(STRING_WRAPPER):
        if lexeme.count(STRING_WRAPPER) == 1:
            state.mode = Mode.STRING
            return Token(TokenType.WORD, lexeme[1:])
        elif lexeme.count(STRING_WRAPPER) == 2 and lexeme.endswith(STRING_WRAPPER):
            return Token(TokenType.END_WORD, lexeme[1:][:-1])

        raise LexError("Word was improperly wrapped in quotes")

    raise LexError("An opening quote should have a space between it and the previous word")


def _tokenize_string_end(lexeme: str, state: State) -> Token:
    """
    Produce a token for the end of a string

    :param lexeme: The last lexeme in a string
    :param state: The current state of the lexer
    :return: A token that represents the end of a string
    :raise LexError: If the given lexeme is not a valid end to a string
    """

    if lexeme.endswith(STRING_WRAPPER) and lexeme.count(STRING_WRAPPER) == 1:
        state.mode = Mode.NORMAL
        return Token(TokenType.END_WORD, lexeme[:-1])

    raise LexError("A closing quote should have a space between it and the previous word")


def _tokenize_string_wrapper(lexeme: str, state: State) -> Token:
    """
    Produce a token upon encountering a string wrapper

    :param lexeme: The lexeme in which a string wrapper was found
    :param state: The current state of the lexer
    :return: A token that represents the given lexeme
    :raise LexError: If the given lexeme is invalid
    """

    if state.mode != Mode.STRING:
        return _tokenize_string_start(lexeme, state)
    else:
        return _tokenize_string_end(lexeme, state)


def _tokenize(lexeme: str, state: State) -> Token:
    """
    Convert the given lexeme into a token of the correct type

    :param lexeme: The lexeme to convert into a token
    :param state: The current state of the lexer
    :return: A token that contains the given lexeme as a value, and has a type based on that lexeme
    :raise LexError: If the given lexeme cannot be matched with any type or is improperly formatted
    """

    if STRING_WRAPPER in lexeme:
        return _tokenize_string_wrapper(lexeme, state)
    elif state.mode == Mode.STRING:
        return Token(TokenType.WORD, lexeme)
    elif lexeme in TOKEN_TYPE_OF_KEYWORD_DICT:
        return Token(TOKEN_TYPE_OF_KEYWORD_DICT[lexeme], lexeme)
    elif lexeme.isnumeric():
        return Token(TokenType.NUMBER, lexeme)

    raise LexError("Unknown lexeme")


def lex(message: str) -> List[Token]:
    """
    Lexically analyze the message

    :param message: The message to analyze
    :return: A series of tokens that each match one of the lexemes in the message
    :raise LexError: When any lexeme is invalid
    """

    command: str = message[len(COMMAND_INDICATOR):]

    lexemes: List[str] = command.split()
    state: State = State(Mode.NORMAL)

    tokens: List[Token] = [_tokenize(lexeme, state) for lexeme in lexemes]
    return tokens
