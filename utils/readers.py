from os.path import isfile
from typing import List, Any, Optional


class Reader:
    """
    Base class for Reader implementation.
    """

    def read(self, *args, **kwargs):
        """
        Base implem of the read function
        """
        raise NotImplementedError


class FileReader(Reader):
    """
    Base class for file Reader implementation

    Support basic file reading
    """

    file = None

    def __init__(self, file: str) -> None:
        assert isfile(file), f"Cannot import file {file}"
        self.file = file

    def read(self, *args, **kwargs) -> str:
        """
        Base implementation of a file read function
        """
        with open(self.file, "r") as f:
            return f.read()


class OneColumnFileReader(FileReader):
    """
    Implementation of a one column data file Reader

    E.g.

    1
    2
    3
    """

    def read(
        self, *args, type_to_cast: Any = None, sort: bool = False, **kwargs
    ) -> List:
        """
        Implementation of a one column data file read function

        :param type_to_cast: Optional type casting for each line
        :param sort: Sort the list
        """
        data = super(OneColumnFileReader, self).read()
        split_data = [line for line in data.splitlines() if line]
        if type_to_cast is not None:
            split_data = list(map(type_to_cast, split_data))
        if sort:
            split_data = sorted(split_data)
        return split_data
