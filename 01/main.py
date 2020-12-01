from typing import Tuple, List

from utils.math import multiply
from utils.readers import OneColumnFileReader
from utils.log import LOG, display_iterable

import itertools

test_reader = OneColumnFileReader("input-test.txt")
test_data = test_reader.read(type_to_cast=int)

reader = OneColumnFileReader("input.txt")
prod_data = reader.read(type_to_cast=int)

data_sources = (("Test data", test_data), ("Prod data", prod_data))


def find_entry_sum_in_list(
    data: List, sum_to_check: int, number_of_elements_in_equation
) -> Tuple[int, ...]:
    """
    Given a list, find the n elements in said list that produced the `sum` value
    when summed

    :param data: Data
    :param sum_to_check: Value to check for
    :param number_of_elements_in_equation: Number of values in the combination
    :return: Matching items
    """

    product_data = [data for _ in range(number_of_elements_in_equation)]

    combinations = list(itertools.product(*product_data))
    for combination in combinations:
        if sum(combination) == sum_to_check:
            return combination


for data_source_name, data_source in data_sources:
    values = find_entry_sum_in_list(data_source, 2020, 2)
    LOG.info(f"Day 0 result 1 - {data_source_name}: {multiply(values)}")

    values = find_entry_sum_in_list(data_source, 2020, 3)
    LOG.info(f"Day 0 result 2 - {data_source_name}: {multiply(values)}")
