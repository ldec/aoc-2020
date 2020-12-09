import re
from copy import copy, deepcopy
from typing import List, Optional, Union, Tuple

from utils.log import LOG
from utils.readers import FileReader, OneColumnFileReader

test_reader = OneColumnFileReader("input-test.txt")
test_data = test_reader.read(type_to_cast=int)

reader = OneColumnFileReader("input.txt")
prod_data = reader.read(type_to_cast=int)

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data),
)


def check_number_validity(preamble: List[int], number: int) -> bool:
    """
    Check if a number can be summed by any different values in the preamble

    :param preamble: Preamble list
    :param number: Number to check
    :return: Number is valid
    """
    for i in preamble:
        for j in preamble:
            if i != j and i + j == number:
                return True
    return False


def check_input(input: List[int], preamble_length: int) -> List[int]:
    """
    Return all invalid numbers in an input list.

    :param input: Input data
    :param preamble_length: Preamble length
    :return: List of invalid number
    """
    non_valid_number = []
    for index, number_to_check in enumerate(input[preamble_length:]):
        # Ensure the index is shifted to the start of the actual numbers
        index += preamble_length
        if not check_number_validity(
            input[index - preamble_length : index], number_to_check
        ):
            non_valid_number.append(number_to_check)

    return non_valid_number


def find_contiguous_set(input: List[int], number_to_find: int) -> List[int]:
    """
    Given a list of number, find the first contiguous set of number with the sum equal
    to number_to_find

    :param input: Number list
    :param number_to_find: Number to search for
    :return: Set numbers
    """

    for i, number_1 in enumerate(input):
        current_sum = number_1
        for j, number_2 in enumerate(input[i + 1 :]):
            current_sum += number_2
            if current_sum == number_to_find:
                return input[i : i + j + 1]
            if current_sum > number_to_find:
                break

    raise Exception("Set not found")


for data_source_name, data_source in data_sources:
    preamble_length = 5
    if data_source_name == "Prod data":
        preamble_length = 25

    invalid_numbers = check_input(data_source, preamble_length=preamble_length)
    LOG.info(f"Day 09 result 1 - {data_source_name}: {invalid_numbers[0]} ")

    contiguous_set = find_contiguous_set(data_source, invalid_numbers[0])

    LOG.info(
        f"Day 09 result 2 - {data_source_name}: {min(contiguous_set) + max(contiguous_set)} "
    )
