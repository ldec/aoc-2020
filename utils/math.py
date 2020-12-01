from typing import Iterable


def multiply(iterable: Iterable) -> int:
    """
    Multiple all numbers in a interables
    :param iterable:
    :return:
    """
    result = 1
    for x in iterable:
        result *= x
    return result
