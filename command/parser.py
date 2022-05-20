from typing import List, Callable, Dict, Tuple

from command.exceptions import ParsingError
from command.expression import Expression, HelpCmdExpr, StringExpr, CommandExpr, AchieveCmdExpr, ViewCmdExpr
from command.keyword_lib import COMMAND_HELP, COMMAND_ACHIEVE, COMMAND_VIEW
from command.token import Token, TokenType


def is_empty(tokens: List[Token]) -> bool:
    """
    :param tokens: The list of tokens to check if it's empty
    :return: True if tokens is empty; otherwise false
    """
    return len(tokens) == 0


def pop_first(tokens: List[Token]) -> Token:
    """
    Removes the first token from the given list of tokens and produces it

    :param tokens: The list of tokens from which to remove and produce the first token
    :return: The first token of the given tokens list
    :raise ParseError: If the given tokens list is empty
    """
    return tokens.pop(0)


def is_of_type(token: Token, token_type: TokenType) -> bool:
    """
    :param token: The token to check the type of
    :param token_type: Check whether or not token is of this type
    :return: True if token is of the given token_type; otherwise, False
    """
    return token.type == token_type


def _call_parser_after_validation(parse_fn: Callable[[List[Token]], any],
                                  tokens: List[Token],
                                  valid_token_types: Tuple[TokenType, ...],
                                  invalid_token_type_msg: str):
    """
    Calls the given parse_fn only if tokens is not empty and the first token is of a valid type

    :param parse_fn: The parsing function to call after validation
    :param tokens: The tokens to validate then call the parser with
    :param valid_token_types: The possible types that the first token can have and be considered valid
    :param invalid_token_type_msg: The error message sent when the first token in tokens has an invalid type
    :return: The expression produced by the given parse_fn
    :raise ParsingError: If the tokens given to the parse function is empty or has a first token with an invalid type
    """

    if is_empty(tokens):
        raise ParsingError("Not enough arguments were given")

    token_type: TokenType = tokens[0].type

    if token_type not in valid_token_types:
        raise ParsingError(invalid_token_type_msg)

    return parse_fn(tokens)


# TODO: Fix typing issues
def _token_type_parser(valid_token_types: Tuple[TokenType, ...], invalid_token_type_msg: str):
    """
    Checks that the tokens given to the parse function are not empty and that the first one has a valid type

    :param valid_token_types: The possible types that the first token can have and be considered valid
    :param invalid_token_type_msg: The error message sent when the first token in tokens has an invalid type
    :return: The decorator for the parse function
    :raise ParsingError: If the tokens given to the parse function is empty or has a first token with an invalid type
    """

    def decorator(parse_fn: Callable[[List[Token]], any]):
        def wrapper(tokens: List[Token]):
            return _call_parser_after_validation(parse_fn, tokens, valid_token_types, invalid_token_type_msg)

        return wrapper

    return decorator


@_token_type_parser((TokenType.WORD, TokenType.END_WORD), "String contained a token that was not a word")
def _parse_word(tokens: List[Token]) -> StringExpr:
    """
    Parse a word token

    :param tokens: The tokens to parse
    :return: A string expression containing this word and any subsequent words
    :raise ParsingError: If token or rest_tokens aren't words
    """

    token: Token = pop_first(tokens)

    if is_of_type(token, TokenType.END_WORD) or is_empty(tokens):
        return StringExpr(token.value, None)

    return StringExpr(token.value, _parse_word(tokens))


# TODO: Create command_parser helper decorator?


@_token_type_parser((TokenType.COMMAND,), "Command requires another command, did not receive one")
def _parse_command(tokens: List[Token]) -> CommandExpr:
    """
    Parse a command token

    :param tokens: The tokens to parse
    :return: A command expression
    :raise Parsing Error: If token is not a command
    """
    token: Token = pop_first(tokens)
    return CommandExpr(token.value)


def _has_optional_param(tokens: List[Token], token_type: TokenType) -> bool:
    """
    :param tokens: The tokens to check for the optional parameter
    :param token_type: The type that the token representing the optional parameter should be of
    :return: True if tokens still contains the command's optional parameter; otherwise, False
    """
    return not is_empty(tokens) and is_of_type(tokens[0], token_type)


def _parse_help_command(tokens: List[Token]) -> HelpCmdExpr:
    """
    Parse a help token

    :param tokens: The tokens to parse
    :return: A help command expression
    :raise ParsingError: If rest_tokens is not empty
    """

    token: Token = pop_first(tokens)
    value: str = token.value

    if _has_optional_param(tokens, TokenType.COMMAND):
        command: CommandExpr = _parse_command(tokens)
        return HelpCmdExpr(value, command)

    return HelpCmdExpr(value)


def _has_optional_string_param(tokens: List[Token]) -> bool:
    """
    :param tokens: The tokens to check for the optional string parameter
    :return: True if tokens still contains the command's optional string parameter; otherwise, False
    """

    return _has_optional_param(tokens, TokenType.WORD) or _has_optional_param(tokens, TokenType.END_WORD)


def _parse_achieve_command(tokens: List[Token]) -> AchieveCmdExpr:
    """
    Parse an achieve token

    :param tokens: The tokens to parse
    :return: An achieve command expression
    :raise ParsingError: If there are parsing errors in the arguments
    """

    token: Token = pop_first(tokens)
    value: str = token.value
    user: StringExpr = _parse_word(tokens)
    achievement_name: StringExpr = _parse_word(tokens)

    if _has_optional_string_param(tokens):
        description_name: StringExpr = _parse_word(tokens)
        return AchieveCmdExpr(value, user, achievement_name, description_name)

    return AchieveCmdExpr(value, user, achievement_name)


def _parse_view_command(tokens: List[Token]) -> ViewCmdExpr:
    """
    Parse a view token

    :param tokens: The tokens to parse
    :return: A list command expression
    :raise ParsingError: If there are parsing errors in the arguments
    """
    token: Token = pop_first(tokens)
    value: str = token.value
    user: StringExpr = _parse_word(tokens)

    if _has_optional_string_param(tokens):
        achievement_name: StringExpr = _parse_word(tokens)
        return ViewCmdExpr(value, user, achievement_name)

    return ViewCmdExpr(value, user)


# TODO: localize to the keyword_lib module
# TODO: switch on enum instead of switch on string consts?
COMMAND_PARSER_DICT: Dict[str, Callable[[List[Token]], CommandExpr]] = {
    COMMAND_HELP: _parse_help_command,
    COMMAND_ACHIEVE: _parse_achieve_command,
    COMMAND_VIEW: _parse_view_command
}


@_token_type_parser((TokenType.COMMAND,), "Command was not started with a command keyword")
def _parse_executing_command(tokens: List[Token]) -> CommandExpr:
    """
    Parse the executing command expression

    :param tokens: The tokens to parse
    :return: An executing command expression
    :raise ParsingError: When the tokens don't conform to the executing command
    """
    token: Token = tokens[0]
    parse_command: Callable[[List[Token]], CommandExpr] = COMMAND_PARSER_DICT[token.value]
    return parse_command(tokens)


def parse(tokens: List[Token]) -> Expression:
    """
    Parse the tokens into an expression

    :param tokens: The tokens to parse
    :return: The expression that matches the tokens
    :raise ParsingError: When the tokens don't conform to any legal expression or no tokens were given
    """

    expr: Expression = _parse_executing_command(tokens)

    if not is_empty(tokens):
        raise ParsingError("Command contained additional arguments")

    return expr
