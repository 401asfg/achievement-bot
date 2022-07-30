COMMAND_PREFIX = ";"

ACHIEVE_NAME = "achieve"
ACHIEVE_DESCRIPTION = "Gives a user a custom achievement"
ACHIEVE_EXAMPLE = COMMAND_PREFIX + ACHIEVE_NAME + " @TheMightyMeercat Meercat Killer"
ACHIEVE_HELP = ACHIEVE_DESCRIPTION + "\n" + ACHIEVE_EXAMPLE

LIST_NAME = "list"
LIST_DESCRIPTION = "Lists all of the achievements that a user has"
LIST_EXAMPLE = COMMAND_PREFIX + LIST_NAME + " @TheMightyMeercat"
LIST_HELP = LIST_DESCRIPTION + "\n" + LIST_EXAMPLE

ACHIEVEMENT_BESTOWER_INDENT = "    "


def member_received_achievement_msg(member_name: str, achievement_name: str) -> str:
    """
    :param member_name: The name of the member who had the given achievement added to them
    :param achievement_name: The name of the achievement that was added to the given member
    :return: A message that states that the given member had the given achievement added to them
    """
    return f"{member_name} has attained the {achievement_name} achievement!"


def member_achievements_header_msg(member_name: str) -> str:
    """
    :param member_name: The name of the member
    :return: A message that is the header for the member of the given member_name's achievements
    """
    return f"{member_name} has attained:\n"
