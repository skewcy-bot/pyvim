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
from .c_mode import match_table as c_mode_match_table
from .r_mode import match_table as r_mode_match_table
from .comms import _is_out_of_bounds, _get_key, _print, _load, _save, _update_screen

match_table: Dict[str, Dict[str, Callable]] = {
    "x": x_mode_match_table,
    "i": i_mode_match_table,
    "c": c_mode_match_table,
    "r": r_mode_match_table,
}


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
        self.file_path = params.get("file_path", "output.txt")
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

    def run(self, file_path: Optional[str] = None) -> None:
        self.gif = True
        self.sleep_time = 0

        if file_path:
            self.file_path = file_path

        _print(self, "pyvim 💕", (0, 0))

        command = ""
        while True:
            command += _get_key()
            ret = self.exec(command)
            if ret:
                command = ""
            elif command.endswith("<Esc>"):
                command = ""

    def exec(self, commands: str) -> bool:
        if self.verbose:
            _print(self, commands, (0, 0))

        index = 0
        while index < len(commands):
            command, new_index = self.match(commands[index:])
            if command:
                command(self, commands[index : index + new_index])
                if self.verbose:
                    _update_screen(self)
                    _print(self, commands, (index, index + new_index))
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

    def __del__(self):
        print("\n\n")
