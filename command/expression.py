from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Expression:
    """
    Any portion of a command
    """
    value: str


@dataclass(frozen=True)
class StringExpr(Expression):
    """
    A string portion of a command
    """
    next_string: Optional['StringExpr']


@dataclass(frozen=True)
class CommandExpr(Expression):
    """
    A command portion of a command
    """
    pass


@dataclass(frozen=True)
class HelpCmdExpr(CommandExpr):
    """
    A help command keyword
    """
    command: CommandExpr = None


@dataclass(frozen=True)
class AchieveCmdExpr(CommandExpr):
    """
    An achieve command keyword
    """
    user: StringExpr
    achievement_name: StringExpr
    achievement_description: StringExpr = None


@dataclass(frozen=True)
class ViewCmdExpr(CommandExpr):
    """
    A view command keyword
    """
    user: StringExpr
    achievement_name: StringExpr = None
