from command.expression import StringExpr, CommandExpr, HelpCmdExpr, AchieveCmdExpr, ViewCmdExpr

# TODO: test
from command.keyword_lib import Command, COMMAND_DICT, COMMAND_HELP, COMMAND_ACHIEVE, COMMAND_VIEW

_author: str


def _interpret_string(expression: StringExpr) -> str:
    string_value: str = expression.value
    next_string: StringExpr = expression.next_string

    if next_string is None:
        return string_value

    return string_value + " " + _interpret(next_string)


def _interpret_command(expression: CommandExpr) -> Command:
    return COMMAND_DICT[expression.value]


def _interpret_help_command(expression: HelpCmdExpr):
    print(COMMAND_HELP)

    if expression.command is not None:
        print(_interpret(expression.command))


def _interpret_achieve_command(expression: AchieveCmdExpr):
    print(COMMAND_ACHIEVE)
    print(_interpret(expression.user))
    print(_interpret(expression.achievement_name))

    if expression.achievement_description is not None:
        print(_interpret(expression.achievement_description))


def _interpret_view_command(expression: ViewCmdExpr):
    print(COMMAND_VIEW)
    print(_interpret(expression.user))

    if expression.achievement_name is not None:
        print(_interpret(expression.achievement_name))


EXPRESSION_INTERPRETER_DICT = {
    StringExpr: _interpret_string,
    CommandExpr: _interpret_command,
    HelpCmdExpr: _interpret_help_command,
    AchieveCmdExpr: _interpret_achieve_command,
    ViewCmdExpr: _interpret_view_command
}


def _interpret(expression):                 # TODO: fix typing
    interpret_expression = EXPRESSION_INTERPRETER_DICT[type(expression)]
    return interpret_expression(expression)


def interpret(expression, author: str):     # TODO: fix typing
    global _author
    _author = author
    _interpret(expression)
