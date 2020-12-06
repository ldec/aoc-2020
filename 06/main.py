from collections import Counter
from typing import List

from utils.log import LOG
from utils.readers import FileReader


class CustomAnswerReader(FileReader):
    """
    Implementation of a Custom answer batch file reader.

    abc

    a
    b
    c
    """

    def read(self, *args, **kwargs) -> List[List[str]]:
        """
        Implementation of a Custom answers file read function.
        """
        data = super(CustomAnswerReader, self).read()

        result = []
        # Split group per group
        groups_answers_raw_data = [line for line in data.split("\n\n") if line]

        # Split per person in group
        for group_answers_raw_data in groups_answers_raw_data:
            group_answers_per_person = [
                line for line in group_answers_raw_data.split("\n") if line
            ]
            result.append(group_answers_per_person)

        return result


test_reader = CustomAnswerReader("input-test.txt")
test_data = test_reader.read()

reader = CustomAnswerReader("input.txt")
prod_data = reader.read()

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data),
)


def count_answers_in_group(answers: List[str]) -> Counter:
    """
    Given a group answers list, count the number of results per question

    :param answers: Group answers
    :return: Counter
    """
    counter = Counter()
    for answer in answers:
        for letter in answer:
            counter[letter] += 1
    return counter


def count_unique_answers(answers_counter: Counter) -> int:
    """
    Given an answer counter, return the number of actually answered questions (doublons
    are not counted)

    :param answers_counter: Answers counter
    :return: Number of answers questions
    """
    return len(answers_counter.keys())


def count_unanimous_answers(answers_counter: Counter, nb_of_persons: int) -> int:
    """
    Given an answer counter, return the number of questions were everyone in the group
    answered

    :param answers_counter: Answers counter
    :return: Number of unanimous answered questions
    """
    count = 0
    for value in answers_counter.values():
        if value == nb_of_persons:
            count += 1
    return count


for data_source_name, data_source in data_sources:
    group_unique_global_count = 0
    group_unanimous_global_count = 0
    for group in data_source:
        answers_counter = count_answers_in_group(group)

        unique_answers_count = count_unique_answers(answers_counter)
        unanimous_answers_count = count_unanimous_answers(answers_counter, len(group))

        group_unique_global_count += unique_answers_count
        group_unanimous_global_count += unanimous_answers_count

    LOG.info(f"Day 06 result 1 - {data_source_name}: {group_unique_global_count} ")

    LOG.info(f"Day 06 result 2 - {data_source_name}: {group_unanimous_global_count} ")
