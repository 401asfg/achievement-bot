from dataclasses import dataclass
from enum import Enum

from command.keyword_lib import COMMANDS, DIRECTIONS
from utils.dict_merging import merge_fromkeys_dicts


class TokenType(Enum):
    """
    The type of a token
    """
    COMMAND = 0
    DIRECTION = 1
    NUMBER = 2
    WORD = 3
    END_WORD = 4


TOKEN_TYPE_OF_KEYWORD_DICT = merge_fromkeys_dicts([COMMANDS, DIRECTIONS],
                                                  [TokenType.COMMAND, TokenType.DIRECTION])


@dataclass(frozen=True)
class Token:
    """
    A distinct lexeme within a command
    """
    type: TokenType
    value: str
