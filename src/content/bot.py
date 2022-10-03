COMMAND_PREFIX = ";"

ACHIEVE_NAME = "achieve"
ACHIEVE_DESCRIPTION = "Gives a user a custom achievement"
ACHIEVE_EXAMPLE = f"{COMMAND_PREFIX}{ACHIEVE_NAME} @TheMightyMeercat Meercat Killer"
ACHIEVE_HELP = f"{ACHIEVE_DESCRIPTION}\n{ACHIEVE_EXAMPLE}"

LIST_NAME = "list"
LIST_DESCRIPTION = "Lists all of the achievements that a user has"
LIST_EXAMPLE = f"{COMMAND_PREFIX}{LIST_NAME} @TheMightyMeercat"
LIST_HELP = f"{LIST_DESCRIPTION}\n{LIST_EXAMPLE}"

ACHIEVEMENT_BESTOWER_INDICATOR = "    -"

BLOCK_END = "```"


def bot_msg(msg: str) -> str:
    """
    :param msg: A message to format
    :return: The given message with the bot's message formatting applied
    """
    return f"{BLOCK_END}{msg}{BLOCK_END}"


def member_received_achievement_msg(member_name: str, achievement_name: str) -> str:
    """
    :param member_name: The name of the member who had the given achievement added to them
    :param achievement_name: The name of the achievement that was added to the given member
    :return: A message that states that the given member had the given achievement added to them
    """
    return f"{member_name} has attained the \"{achievement_name}\" achievement!"


def achievement_listing(achievement_name: str, bestower_name: str) -> str:
    """
    :param achievement_name: The name of the achievement that the listing is of
    :param bestower_name: The name of the user who bestowed the achievement
    :return: A listing of an achievement with the given achievement_name and the given bestower_name
    """
    return f"\n{achievement_name}\n{ACHIEVEMENT_BESTOWER_INDICATOR}{bestower_name}"


def member_achievement_list_msg(member_name: str, achievement_list_msg: str) -> str:
    """
    :param member_name: The name of the member
    :param achievement_list_msg: The a message containing the list of achievements the member of the given member_name
    has
    :return: A message containing the given member_name and the given achievement_list_msg
    """
    return f"{member_name} has achieved:\n{achievement_list_msg}"


def member_has_no_achievements_msg(member_name: str) -> str:
    """
    :param member_name: The name of the member
    :return: A message stating that the member of the given member_name has no achievements
    """
    return f"{member_name} has no achievements"
