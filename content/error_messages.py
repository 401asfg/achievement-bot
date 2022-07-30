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
