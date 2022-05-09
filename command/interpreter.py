from command.expression import NumberExpr, StringExpr, DirectionExpr, HelpCmdExpr, CharacterCmdExpr, \
    MoveCmdExpr, CommandExpr
from command.keyword_lib import Direction, DIRECTION_DICT, Command, COMMAND_DICT, COMMAND_HELP, COMMAND_CHARACTER, \
    COMMAND_MOVE

# TODO: test

_author: str


def _interpret_number(number_expr: NumberExpr) -> int:
    return int(number_expr.value)


def _interpret_string(string_expr: StringExpr) -> str:
    string_value: str = string_expr.value
    next_string: StringExpr = string_expr.next_string

    if next_string is None:
        return string_value

    return string_value + " " + _interpret(next_string)


def _interpret_direction(direction_expr: DirectionExpr) -> Direction:
    return DIRECTION_DICT[direction_expr.value]


def _interpret_command(command_expr: CommandExpr) -> Command:
    return COMMAND_DICT[command_expr.value]


def _interpret_help_command(help_cmd_expr: HelpCmdExpr):
    print(COMMAND_HELP)

    if help_cmd_expr.command is not None:
        print(_interpret(help_cmd_expr.command))


def _interpret_character_command(character_cmd_expr: CharacterCmdExpr):
    global _author

    print(_author)
    print(COMMAND_CHARACTER)
    print(_interpret(character_cmd_expr.name))


def _interpret_move_command(move_cmd_expr: MoveCmdExpr):
    print(COMMAND_MOVE)
    print(_interpret(move_cmd_expr.direction))
    print(_interpret(move_cmd_expr.distance))


EXPRESSION_INTERPRETER_DICT = {
    NumberExpr: _interpret_number,
    StringExpr: _interpret_string,
    DirectionExpr: _interpret_direction,
    CommandExpr: _interpret_command,
    HelpCmdExpr: _interpret_help_command,
    CharacterCmdExpr: _interpret_character_command,
    MoveCmdExpr: _interpret_move_command
}


def _interpret(expression):                 # TODO: fix typing
    interpret_expression = EXPRESSION_INTERPRETER_DICT[type(expression)]
    return interpret_expression(expression)


def interpret(expression, author: str):     # TODO: fix typing
    global _author
    _author = author
    _interpret(expression)
