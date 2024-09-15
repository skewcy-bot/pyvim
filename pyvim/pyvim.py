"""
Author: <Chuanyu> (skewcy@gmail.com)
pyvim.py (c) 2024
Desc: description
Created:  2024-07-21T16:32:14.272Z
"""

from time import sleep
from typing import Callable, Tuple, Optional, Dict
from copy import deepcopy
import re

from .x_mode import match_table as x_mode_match_table
from .i_mode import match_table as i_mode_match_table
from .comms import _is_out_of_bounds, get_key

match_table: Dict[str, Dict[str, Callable]] = {
    "x": x_mode_match_table,
    "i": i_mode_match_table,
}


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


REFRESH_RATE = 1


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


class Buffer:
    def __init__(self, data: str) -> None:
        self.data = [list(line) for line in data.split("\n")]
        self.length = len(self.data)
        self.width = [len(line) for line in self.data]

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.data)


class Cursor:
    def __init__(self, row: int, col: int, buffer: Optional[Buffer] = None) -> None:
        if row < 0 and buffer:
            row = buffer.length + row
        self.row = row

        if col < 0 and buffer:
            col = buffer.width[row] + col
        self.col = col


class Screen:
    def __init__(self, top: int = 0, lines: int = 5) -> None:
        self.top = top
        self.lines = lines


"""
Vim emulator.

data: str
    The initial buffer content.
row: int
    The initial cursor row.
col: int
    The initial cursor column.
Params:
    - verbose: print command and buffer after each command
    - animation: print buffer after each command
    - interactive: wait for user input after each command
"""


class VimEmulator:
    def __init__(
        self,
        data: str,
        row: int = 0,
        col: int = 0,
        params: Optional[Dict[str, bool]] = None,
    ) -> None:
        self._buffer = Buffer(data=data)
        self._cursor = Cursor(row, col, self._buffer)
        self._screen = Screen(top=0, lines=self.length)
        if _is_out_of_bounds(self):
            raise ValueError("Cursor out of bounds")

        self.mode = "x"  ## x: normal, i: insert, v: visual, r: replace, c: command

        if params is None:
            params = {}

        self.verbose = params.get("verbose", True)
        self.gif = params.get("gif", False)
        self.sleep_time = params.get("sleep_time", 1)
        self._cmd: list[str] = []

    width = delegate_property("_buffer", "width")
    length = delegate_property("_buffer", "length")
    row = delegate_property("_cursor", "row")
    col = delegate_property("_cursor", "col")
    buffer = delegate_property("_buffer", "data")

    def __getitem__(self, key):
        return self._buffer.data[key]

    def __setitem__(self, key, value):
        self._buffer.data[key] = value

    def run(self) -> None:
        self.gif = True
        self.sleep_time = 0
        self.print("pyvim 💕", (0, 0))

        command = ""
        while True:
            command += get_key()
            ret = self.exec(command)
            if ret:
                command = ""
            elif command.endswith("<Esc>"):
                command = ""

    def exec(self, commands: str) -> bool:
        if self.verbose:
            self.print(commands, (0, 0))

        index = 0
        while index < len(commands):
            command, new_index = self.match(commands[index:])
            if command:
                command(self, commands[index : index + new_index])
                if self.verbose:
                    self.print(commands, (index, index + new_index))
                    if self.gif:
                        sleep(self.sleep_time)
                self._cmd.append(commands[index : index + new_index])
                index += new_index
            else:
                return False
        return True

    def match(self, commands: str) -> Tuple[Optional[Callable], int]:
        for pattern, command in match_table[self.mode].items():
            result = re.search("^" + pattern, commands)
            if result:
                return command, result.end()
        return None, 0

    def print(self, cl: str, comm_range: tuple[int, int], cursor: bool = True) -> None:
        _comm = (
            cl[: comm_range[0]]
            + bcolors.FAIL
            + cl[comm_range[0] : comm_range[1]]
            + bcolors.ENDC
            + cl[comm_range[1] :]
        )

        _msg = deepcopy(self._buffer)

        ## Set cursor color
        if cursor and (self.mode == "x" or self.mode == "i"):
            if self.mode == "x":
                _cursor_color = 4  # blue
            elif self.mode == "i":
                _cursor_color = 2  # green
            if not len(_msg.data[self.row]):
                _msg.data[self.row].append(f"\033[34;4{_cursor_color}m \033[m")
            else:
                _msg.data[self._cursor.row][self._cursor.col] = (
                    f"\033[34;4{_cursor_color}m"
                    + _msg.data[self._cursor.row][self._cursor.col]
                    + "\033[m"
                )

        _line_number_width = len(str(self._screen.top + self._screen.lines))

        _split = (
            bcolors.OKBLUE
            + "-" * (max([len(line) for line in _msg.data]) + _line_number_width + 1)
            + bcolors.ENDC
        )

        if self.gif:
            print(chr(27) + "[2J")

        print("Exec: ", _comm)

        print(_split)

        for _line_index in range(
            self._screen.top, self._screen.top + self._screen.lines
        ):
            print(
                bcolors.WARNING
                + str(_line_index + 1)
                + " " * (_line_number_width - len(str(_line_index)))
                + bcolors.ENDC,
                end=" ",
            )
            print("".join(_msg.data[_line_index]))

        print(_split)

    def __del__(self):
        print("\n\n")
