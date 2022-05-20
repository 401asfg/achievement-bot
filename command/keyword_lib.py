from enum import Enum

###### SYNTAX ######

STRING_WRAPPER = "\""
COMMAND_INDICATOR = ';'

####################


###### COMMANDS #######

COMMAND_HELP = "help"
COMMAND_ACHIEVE = "achieve"
COMMAND_VIEW = "view"

COMMANDS = (COMMAND_HELP, COMMAND_ACHIEVE, COMMAND_VIEW)


class Command(Enum):
    """
    A command that can be executed
    """
    HELP = 0
    ACHIEVE = 1
    VIEW = 2


COMMAND_DICT = {
    COMMAND_HELP: Command.HELP,
    COMMAND_ACHIEVE: Command.ACHIEVE,
    COMMAND_VIEW: Command.VIEW
}

#######################
