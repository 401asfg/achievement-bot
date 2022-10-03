from typing import List

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
ACHIEVEMENT_BESTOWER_BULLET = "- "

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


# TODO: test/move parts into model?


def member_achievement_list_msg(member_name: str, achievement_names: List[str], bestower_names: List[str]) -> str:
    """
    Produces a message that contains the given member_name, the given achievement_names, and the given bestower_names;
    The achievement_names list and the bestower_names list should have equal lengths

    :param member_name: The name of the member
    :param achievement_names: The names of the member's achievements
    :param bestower_names: The names of the bestowers of each of the member's achievements
    :return: A message containing the given member_name, the achievement_names, and the bestower_names
    """

    achievement_list_msg = f"{member_name} has achieved:\n"

    for i in range(len(achievement_names)):
        achievement_list_msg += "\n" + achievement_names[i] + "\n" + ACHIEVEMENT_BESTOWER_INDICATOR + bestower_names[i]

    return achievement_list_msg


def member_no_achievements_msg(member_name: str) -> str:
    """
    :param member_name: The name of the member
    :return: A message stating that the member of the given member_name has no achievements
    """
    return f"{member_name} has no achievements"
