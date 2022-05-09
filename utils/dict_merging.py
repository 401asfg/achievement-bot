from typing import List


def merge_dict(dict1: dict, dict2: dict) -> dict:
    """
    Merge two dictionaries into one

    :param dict1: One of the dictionaries to merge
    :param dict2: One of the dictionaries to merge
    :return: The new dictionary, resulting from merging dict1 and dict2
    """

    merged_dict: dict = {}
    merged_dict.update(dict1)
    merged_dict.update(dict2)

    return merged_dict


def merge_dicts(dicts: List[dict]) -> dict:
    """
    Merge multiple dictionaries into one

    :param dicts: The dictionaries to merge
    :return: The new dictionary, resulting from merging the dicts
    """

    merged_dict: dict = {}

    for dictionary in dicts:
        merged_dict = merge_dict(merged_dict, dictionary)

    return merged_dict


def merge_fromkeys_dicts(key_sets: List[List[any]], values: List[any]) -> dict:
    """
    Create multiple new dictionaries, each using a different one of the key_sets and one of the values, and merge them
    into one

    :param key_sets: Each dictionary will use one of these sets as its keys; the length of this list must be equal to
    that of values
    :param values: Each dictionary will use one of these values as its value for all of its keys; the length of this
    list must be equal to that of values
    :return: The new dictionary, resulting from merging all the dictionaries created with the key_sets and values
    :raise ValueError: If the lengths of key_sets and values aren't equal
    """

    if len(key_sets) != len(values):
        raise ValueError("Attempted to build dictionaries from sets of keys and a set of values that had different "
                         "lengths")

    dicts: List[dict] = [dict.fromkeys(key_set, value) for key_set, value in zip(key_sets, values)]
    return merge_dicts(dicts)
