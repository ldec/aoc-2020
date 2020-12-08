import re
from copy import copy, deepcopy
from typing import List, Optional, Union

from utils.log import LOG
from utils.readers import FileReader


END_OF_TAPE = object


class InfiniteLoopException(Exception):
    pass


class ProgramReader(FileReader):
    """
    Implementation of a program file reader.

    nop +0
    acc +1
    jmp +4
    """

    def read(self, *args, **kwargs) -> List[List[str]]:
        """
        Implementation of a program file read function.
        """
        data = super(ProgramReader, self).read()

        lines = [line.split(" ") for line in data.split("\n") if line]
        result = []
        for instruction, value in lines:
            operation = "add"
            if value.startswith("-"):
                operation = "sub"
            result.append([instruction, operation, int(value[1:])])

        return result


class Tape(object):
    visited_index = None
    accumulator = None

    def __init__(self, tape: List) -> None:
        self.visited_index = []
        self.__tape = tape
        self.accumulator = 0

    def __getitem__(self, index: int) -> Optional[str]:
        if index in self.__tape:
            return self.__tape[index]
        else:
            return None

    def check_tape_validity(self) -> None:
        """
        Check that at any moment during a tape execution, no instruction was ever
        visited twice.

        :return: Tape is valid
        """
        visited_set = set(self.visited_index)
        if len(visited_set) != len(self.visited_index):
            raise InfiniteLoopException()

    def execute_instruction(self, index: int) -> Union[int, END_OF_TAPE]:
        """
        Given an index, execute the current instruction and return the index of the next
        one.

        If the execution was the last, return END_OF_TAPE

        :param index: Index of instruction to execute
        :return: Index of next instruction to execute of END_OF_TAPE
        """
        try:
            instruction_list = self.__tape[index]
        except IndexError:
            return END_OF_TAPE

        instruction, operation, value = instruction_list

        self.visited_index.append(index)
        self.check_tape_validity()

        if instruction == "nop" or instruction == "acc":
            if instruction == "acc":
                if operation == "add":
                    self.accumulator += value
                else:
                    self.accumulator -= value

            return index + 1

        elif instruction == "jmp":
            if operation == "add":
                return index + value
            else:
                return index - value

        raise Exception(f"Unknown instruction {instruction}")

    def execute_program(self, accumulator: int = 0):
        """
        Given
        :param accumulator:
        :return:
        """
        self.accumulator = accumulator
        index = 0
        while index is not END_OF_TAPE:
            index = self.execute_instruction(index)


def change_tape(tape_input, index_to_change):
    """
    Given an tape input and an index to change, check if permuting nop and jmp
    fixes the program.

    :param tape_input: Original tape input
    :param index_to_change: Index to permute instruction
    :return: Program is fixed, current accumulator
    """
    instruction_at_index = tape_input[index_to_change][0]
    if instruction_at_index == "nop":
        tape_input[index_to_change][0] = "jmp"
    else:
        tape_input[index_to_change][0] = "nop"

    # Create & check modified tape
    tape = Tape(tape_input)
    try:
        tape.execute_program()
    except InfiniteLoopException:
        return False, tape.accumulator

    return True, tape.accumulator


test_reader = ProgramReader("input-test.txt")
test_data = test_reader.read()

reader = ProgramReader("input.txt")
prod_data = reader.read()

data_sources = (
    ("Test data", test_data),
    ("Prod data", prod_data),
)

for data_source_name, data_source in data_sources:
    tape = Tape(data_source)
    try:
        tape.execute_program()
    except InfiniteLoopException:
        pass

    LOG.info(f"Day 08 result 1 - {data_source_name}: accumulator: {tape.accumulator} ")

    for index in range(1, len(data_source) - 1):
        fixed, accumulator = change_tape(deepcopy(data_source), index)
        if fixed:
            LOG.info(
                f"Day 08 result 1 - {data_source_name}: Index {index + 1}, accumulator: {accumulator} "
            )
            break
