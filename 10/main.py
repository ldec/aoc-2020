from collections import Counter
from collections import Counter
from typing import List, Tuple

from utils.log import LOG
from utils.readers import OneColumnFileReader

OUTLET_JOLT_RATING = 0
RATING_TOLERANCE = 3

test_reader = OneColumnFileReader("input-test.txt")
test_data = test_reader.read(type_to_cast=int, sort=True)

test_reader = OneColumnFileReader("input-test2.txt")
test_data2 = test_reader.read(type_to_cast=int, sort=True)

reader = OneColumnFileReader("input.txt")
prod_data = reader.read(type_to_cast=int, sort=True)

data_sources = (
    ("Test data", test_data),
    ("Test data 2 ", test_data2),
    ("Prod data", prod_data),
)


def find_adapter_by_ratings(adapters_list: List[int], jolt_ratings: List[int]) -> int:
    """
    Find the first adapter corresponding to any of the rating

    :param adapters_list: Adapter list
    :param jolt_ratings: Jolt rating
    :return:
    """
    for jolt_rating in jolt_ratings:
        if jolt_rating in adapters_list:
            return jolt_rating

    raise Exception(f"No adapter found for ratings {jolt_ratings}")


def find_adapter_by_output_rating(
    adapters_list: List[int], requested_output_jolt: int
) -> int:
    """
    Given an output jolt, find the first corresponding adapter

    :param adapters_list: Adapter list
    :param requested_output_jolt: Ouput rating
    :return: First adapter found
    """
    accepted_output_jolt_ratings = list(
        range(requested_output_jolt + 1, requested_output_jolt + RATING_TOLERANCE + 1)
    )
    return find_adapter_by_ratings(adapters_list, accepted_output_jolt_ratings)


def find_adapter_by_input_rating(
    adapters_list: List[int], requested_input_jolt: int
) -> int:
    """
    Given an input jolt, find the first corresponding adapter

    :param adapters_list: Adapter list
    :param requested_input_jolt: Input rating
    :return: First adapter found
    """
    accepted_input_jolt_rating = list(
        range(requested_input_jolt - RATING_TOLERANCE, requested_input_jolt)
    )
    return find_adapter_by_ratings(adapters_list, accepted_input_jolt_rating)


def find_list_of_adapters_for_device(
    adapter_list: List[int], device_input_jolt: int
) -> Tuple[List[Tuple[int, int]], Counter]:
    """
    Given a list of adapters, find the list of adapters arrangements
    (without wasting any) and the total number of rating difference in the conversion
    process.

    :param adapter_list: Adapter list
    :param device_input_jolt: Device jolt rating
    :return: Adapter list, rating difference counter
    """
    accepted_input_jolt_rating = list(
        range(device_input_jolt - RATING_TOLERANCE, device_input_jolt)
    )

    found = False
    current_adapter = 0
    adapters_list = []
    rating_difference_counter = Counter()
    while not found:
        last_step_adapter = current_adapter
        current_adapter = find_adapter_by_output_rating(adapter_list, current_adapter)

        rating_difference = current_adapter - last_step_adapter
        rating_difference_counter[rating_difference] += 1
        adapters_list.append((current_adapter, rating_difference))

        if current_adapter in accepted_input_jolt_rating:
            rating_difference_counter[3] += 1
            return adapters_list, rating_difference_counter

    raise Exception(f"Could not find adapters list for rating {device_input_jolt}")


for data_source_name, data_source in data_sources:
    device_jolt_rating = max(data_source) + 3

    adapters_list, rating_difference_counter = find_list_of_adapters_for_device(
        data_source, device_jolt_rating
    )

    LOG.info(
        f"Day 10 result 1 - {data_source_name}: {rating_difference_counter[1] * rating_difference_counter[3]} "
    )
