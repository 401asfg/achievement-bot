from dataclasses import dataclass
from enum import Enum

from command.keyword_lib import COMMANDS
from utils.dict_merging import merge_fromkeys_dicts


class TokenType(Enum):
    """
    The type of a token
    """
    COMMAND = 0
    WORD = 1
    END_WORD = 2


TOKEN_TYPE_OF_KEYWORD_DICT = merge_fromkeys_dicts([COMMANDS],
                                                  [TokenType.COMMAND])


@dataclass(frozen=True)
class Token:
    """
    A distinct lexeme within a command
    """
    type: TokenType
    value: str
