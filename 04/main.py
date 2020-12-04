import re
from typing import List

from utils.log import LOG
from utils.readers import FileReader

HEIGHT_REGEX = re.compile(r"(\d+)(in|cm)")
HAIR_COLOR_REGEX = re.compile(r"#[0-9a-f]{6}")


class PassportBatchReader(FileReader):
    """
    Implementation of a Passport batch file reader.

    E.g.

    ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929
    """

    def read(self, *args, **kwargs) -> List[List[str]]:
        """
        Implementation of a Passport batch file read function.
        """
        data = super(PassportBatchReader, self).read()

        # Split passport per passport
        passport_raw_data = [
            line.replace("\n", " ") for line in data.split("\n\n") if line
        ]

        # Split each passport components
        passport_raw_split_data = [
            passport.split(" ") for passport in passport_raw_data
        ]

        return passport_raw_split_data


test_reader = PassportBatchReader("input-test.txt")
test_data = test_reader.read()

reader = PassportBatchReader("input.txt")
prod_data = reader.read()

data_sources = (("Test data", test_data), ("Prod data", prod_data))


# Validators
def no_validation(value: str) -> bool:
    """
    Dummy validator

    :param value: Value to check
    :return: Always True
    """
    return True


def validate_byr(value: str) -> bool:
    """
    Birth Year validator

    :param value: Value to check
    :return: Value is correct
    """
    return 1920 <= int(value) <= 2002


def validate_iyr(value: str) -> bool:
    """
    Issue Year validator

    :param value: Value to check
    :return: Value is correct
    """
    return 2010 <= int(value) <= 2020


def validate_eyr(value: str) -> bool:
    """
    Expiration Year validator

    :param value: Value to check
    :return: Value is correct
    """
    return 2020 <= int(value) <= 2030


def validate_hgt(value: str) -> bool:
    """
    Height validator

    :param value: Value to check
    :return: Value is correct
    """
    try:
        value, unit = HEIGHT_REGEX.match(value).groups()
    except AttributeError:
        return False
    if unit == "cm":
        return 150 <= int(value) <= 193
    return 59 <= int(value) <= 76


def validate_hcl(value: str) -> bool:
    """
    Hair Color validator

    :param value: Value to check
    :return: Value is correct
    """
    return bool(HAIR_COLOR_REGEX.match(value))


def validate_ecl(value: str) -> bool:
    """
    Eye Color validator

    :param value: Value to check
    :return: Value is correct
    """
    return value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth",)


def validate_pid(value: str) -> bool:
    """
    Passport ID validator

    :param value: Value to check
    :return: Value is correct
    """
    return value.isdecimal() and len(value) == 9


def raw_component_passport_to_parsed(passport_raw_components: List[str]) -> dict:
    """
    Given a list of a passport raw components, return the parsed passport data.

    :param passport_raw_components:
    :return: Parsed passport data
    """
    passport_data = {}
    for passport_raw_component in passport_raw_components:
        if passport_raw_component:
            field, value = passport_raw_component.split(":")
            passport_data[field] = value
    return passport_data


def validate_raw_passports(raw_passports: List[List[str]], compulsory: dict):
    """
    Count the number of valid passports in a passport dump

    :param raw_passports: Raw passport data
    :param compulsory: dict of compulsory check alongside validation checks
    :return: Number of valid passports
    """
    valid_count = 0
    for raw_passport in raw_passports:
        passport_data = raw_component_passport_to_parsed(raw_passport)

        is_valid = True
        # Check if any compulsory value is missing
        for compulsory_field in compulsory.keys():
            if compulsory_field not in passport_data:
                is_valid = False
                break

        # Check that each value is correct against its validating func
        for field, value in passport_data.items():
            if field in compulsory and not compulsory[field](value):
                is_valid = False
                break

        if is_valid:
            valid_count += 1

    return valid_count


for data_source_name, data_source in data_sources:
    compulsory_1 = {
        "byr": no_validation,
        "iyr": no_validation,
        "eyr": no_validation,
        "hgt": no_validation,
        "hcl": no_validation,
        "ecl": no_validation,
        "pid": no_validation,
    }

    LOG.info(
        f"Day 04 result 1 - {data_source_name}: {validate_raw_passports(data_source, compulsory_1)}"
    )

    compulsory_2 = {
        "byr": validate_byr,
        "iyr": validate_iyr,
        "eyr": validate_eyr,
        "hgt": validate_hgt,
        "hcl": validate_hcl,
        "ecl": validate_ecl,
        "pid": validate_pid,
    }
    LOG.info(
        f"Day 04 result 2 - {data_source_name}: {validate_raw_passports(data_source, compulsory_2)}"
    )
