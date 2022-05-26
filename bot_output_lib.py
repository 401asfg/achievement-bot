COMMAND_PREFIX = ";"

ACHIEVE_NAME = "achieve"
ACHIEVE_DESCRIPTION = "Gives a user a custom achievement"
ACHIEVE_EXAMPLE = COMMAND_PREFIX + ACHIEVE_NAME + " @TheMightyMeercat Meercat Killer"
ACHIEVE_HELP = ACHIEVE_DESCRIPTION + "\n" + ACHIEVE_EXAMPLE

LIST_NAME = "list"
LIST_DESCRIPTION = "Lists all of the achievements that a user has"
LIST_EXAMPLE = COMMAND_PREFIX + LIST_NAME + " @TheMightyMeercat"
LIST_HELP = LIST_DESCRIPTION + "\n" + LIST_EXAMPLE

ADDED_ACHIEVEMENT_TO_SELF_ERROR_MSG = "You cannot add an achievement to yourself"


def member_not_in_server_error_msg(member_name: str) -> str:
    """
    :param member_name: The name of the member that is not in the server
    :return: An error message for when a member is not in the server
    """
    return f"{member_name} is not in this server"


def member_already_has_achievement_error_msg(member_name: str, achievement_name: str) -> str:
    """
    :param member_name: The name of the member
    :param achievement_name: The name of the achievement that the member already has
    :return: An error message for when a member already has an achievement
    """
    return f"{member_name} already has the {achievement_name} achievement"


def member_achievements_header_msg(member_name: str) -> str:
    """
    :param member_name: The name of the member
    :return: A message that is the header for the member of the given member_name's achievements
    """
    return f"{member_name} has attained:\n"
