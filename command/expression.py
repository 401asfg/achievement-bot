from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Expression:
    """
    Any portion of a command
    """
    value: str


@dataclass(frozen=True)
class NumberExpr(Expression):
    """
    A number portion of a command
    """
    pass


@dataclass(frozen=True)
class StringExpr(Expression):
    """
    A string portion of a command
    """
    next_string: Optional['StringExpr']


@dataclass(frozen=True)
class DirectionExpr(Expression):
    """
    A direction portion of a command
    """
    pass


@dataclass(frozen=True)
class CommandExpr(Expression):
    """
    A command portion of a command
    """
    pass


@dataclass(frozen=True)
class HelpCmdExpr(CommandExpr):
    """
    A help command keyword at the start of a command
    """
    command: CommandExpr = None


@dataclass(frozen=True)
class CharacterCmdExpr(CommandExpr):
    """
    A character command keyword at the start of a command
    """
    name: StringExpr


@dataclass(frozen=True)
class MoveCmdExpr(CommandExpr):
    """
    A move command keyword at the start of a command
    """
    direction: DirectionExpr
    distance: NumberExpr = NumberExpr("1")
