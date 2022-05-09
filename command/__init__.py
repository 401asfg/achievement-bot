from command import exceptions


# TODO: make state/context in the lexer and interpreter module wide variables


def is_command(message: str) -> bool:
    from command.keyword_lib import COMMAND_INDICATOR
    return message.startswith(COMMAND_INDICATOR)


def interpret_command(message: str, author: str):
    """
    Interpret the given message as a command

    :param message: The message to interpret
    :param author: The message's author
    :raise LexError: When there is an invalid lexeme in the message
    :raise ParsingError: When a series of tokens don't conform to any abstract syntax tree
    """

    from command.lexer import lex
    from command.parser import parse
    from command.interpreter import interpret

    tokens = lex(message)
    expression = parse(tokens)
    interpret(expression, author)
