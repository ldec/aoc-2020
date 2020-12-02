import re
from typing import List
from collections import Counter

from utils.log import LOG
from utils.readers import FileReader

PASSWORD_DATABASE_LINE_REGEX = re.compile("(\d+)-(\d+) (\w): (\w+)")


class PasswordDatabaseConditions:
    """
    Representation of a condition object.
    """

    min = None
    max = None
    letter = None

    def __init__(self, min_value: str, max_value: str, letter: str) -> None:
        self.min = int(min_value)
        self.max = int(max_value)
        self.letter = letter

    def validate_password(self, password: str, old_rule: bool = False):
        """
        Check the password against two possible rules.

        1: Count of given letter in the password is between min & max.
        2: Presence of given letter on either index min or max but not both.

        :param password: Password to check
        :param old_rule: Use the first rule
        :return: Password is valid
        """
        if old_rule:
            return self.min <= password.count(self.letter) <= self.max
        else:
            match_min = password[self.min - 1] == self.letter
            match_max = password[self.max - 1] == self.letter
            return match_min ^ match_max


class PasswordDatabaseReader(FileReader):
    """
    Implementation of a password database file reader.

    E.g.

    1-3 a: abcde
    1-3 b: cdefg
    2-9 c: ccccccccc
    """

    def read(self, *args, **kwargs) -> List:
        """
        Implementation of a one column data file read function.
        """
        data = super(PasswordDatabaseReader, self).read()

        result = []

        for line in data.splitlines():
            if line:
                match = PASSWORD_DATABASE_LINE_REGEX.match(line)
                if match is not None:
                    result.append(match.groups())
                else:
                    raise Exception(f"Could not read database line {line}")

        return result


test_reader = PasswordDatabaseReader("input-test.txt")
test_data = test_reader.read()

reader = PasswordDatabaseReader("input.txt")
prod_data = reader.read()

data_sources = (("Test data", test_data), ("Prod data", prod_data))


def validate_database_line(
    min_value: str, max_value: str, letter: str, password: str, old_rule: bool = False
):
    """
    Validate a split database line.

    :param min_value: Condition mix value
    :param max_value: Condition max value
    :param letter: Condition letter
    :param password: Password
    :param old_rule: Use the first rule
    :return: Password is valid
    """
    condition = PasswordDatabaseConditions(min_value, max_value, letter)
    return condition.validate_password(password, old_rule=old_rule)


for data_source_name, data_source in data_sources:
    values = [validate_database_line(*line, old_rule=True) for line in data_source]
    LOG.info(f"Day 0 result 1 - {data_source_name}: {Counter(values)[True]}")

    values = [validate_database_line(*line) for line in data_source]
    LOG.info(f"Day 0 result 2 - {data_source_name}: {Counter(values)[True]}\n")
