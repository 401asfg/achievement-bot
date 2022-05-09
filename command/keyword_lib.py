from enum import Enum

###### SYNTAX ######

STRING_WRAPPER = "\""
COMMAND_INDICATOR = ';'

####################


###### COMMANDS #######

COMMAND_HELP = "help"
COMMAND_CHARACTER = "character"
COMMAND_MOVE = "move"

COMMANDS = (COMMAND_HELP, COMMAND_CHARACTER, COMMAND_MOVE)


class Command(Enum):
    """
    A command that can be executed
    """
    HELP = 0
    CHARACTER = 1
    MOVE = 2


COMMAND_DICT = {
    COMMAND_HELP: Command.HELP,
    COMMAND_CHARACTER: Command.CHARACTER,
    COMMAND_MOVE: Command.MOVE
}

#######################


###### DIRECTIONS ######

DIRECTION_UP = "up"
DIRECTION_DOWN = "down"
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"

DIRECTIONS = (DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT)


class Direction(Enum):
    """
    A direction that can be moved in
    """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


DIRECTION_DICT = {
    DIRECTION_UP: Direction.UP,
    DIRECTION_DOWN: Direction.DOWN,
    DIRECTION_LEFT: Direction.LEFT,
    DIRECTION_RIGHT: Direction.RIGHT
}

########################
