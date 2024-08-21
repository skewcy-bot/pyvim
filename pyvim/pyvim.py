"""
Author: <Chuanyu> (skewcy@gmail.com)
vim_emulator.py (c) 2024
Desc: description
Created:  2024-07-21T16:32:14.272Z
"""

from time import sleep
from typing import Callable, Tuple, Optional
from copy import deepcopy
import re

from .normal import match_table


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


"""
Support nested object properties (getter and setter).
"""


def delegate_property(attribute_name, property_name):
    """Creates a property that delegates to an attribute of a nested object."""

    def getter(self):
        return getattr(getattr(self, attribute_name), property_name)

    def setter(self, value):
        setattr(getattr(self, attribute_name), property_name, value)

    return property(getter, setter)


class Cursor:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col


class Buffer:
    def __init__(self, data: str) -> None:
        self.data = [list(line) for line in data.split("\n")]
        self.length = len(self.data)
        self.width = [len(line) for line in self.data]

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.data)


class VimEmulator:
    def __init__(self, data: str) -> None:
        self._cursor = Cursor(0, 0)
        self._buffer = Buffer(data=data)

        self.mode = "x"  ## x: normal, i: insert, v: visual, r: replace, c: command

        self.verbose = True
        self.gif = False

    width = delegate_property("_buffer", "width")
    length = delegate_property("_buffer", "length")
    row = delegate_property("_cursor", "row")
    col = delegate_property("_cursor", "col")
    buffer = delegate_property("_buffer", "data")

    def __getitem__(self, key):
        return self._buffer.data[key]

    def __setitem__(self, key, value):
        self._buffer.data[key] = value

    def exec(self, commands: str) -> bool:
        if self.verbose:
            self.print(commands, (0, 0))

        index = 0
        while index < len(commands):
            command, new_index = self.match(commands[index:])
            if command:
                command(self, *commands[index + 1 : index + new_index])
                if self.verbose:
                    self.print(commands, (index, index + new_index))
                index += new_index
            else:
                assert False, f"Invalid command: {commands[index:]}"
        return True

    def match(self, commands: str) -> Tuple[Optional[Callable], int]:
        for pattern, command in match_table.items():
            result = re.search("^" + pattern, commands)
            if result:
                return command, result.end()
        return None, 0

    def print(self, cl: str, range: tuple[int, int]) -> None:
        _msg = deepcopy(self._buffer)
        if self.mode == "x":
            if not len(_msg.data[self.row]):
                _msg.data[self.row].append("█")
            else:
                _msg.data[self._cursor.row][self._cursor.col] = "█"

        _comm = (
            cl[: range[0]]
            + bcolors.FAIL
            + cl[range[0] : range[1]]
            + bcolors.ENDC
            + cl[range[1] :]
        )
        _split = (
            bcolors.OKBLUE + "-" * [len(line) for line in _msg.data][0] + bcolors.ENDC
        )
        print("Exec: ", _comm)
        print(_split)
        print(_msg)
        print(_split)

        if self.gif:
            sleep(1)
            print(chr(27) + "[2J")

    def __del__(self):
        print("\n\n")
