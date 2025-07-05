"""
Author: <Chuanyu> (skewcy@gmail.com)
pyvim.py (c) 2024
Desc: description
Created:  2024-07-21T16:32:14.272Z
"""

from time import sleep
from typing import Callable, Tuple, Optional, Dict, Union, Any
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


def delegate_property(attribute_name: str, property_name: str) -> property:
    """Creates a property that delegates to an attribute of a nested object."""

    def getter(self: Any) -> Any:
        return getattr(getattr(self, attribute_name), property_name)

    def setter(self: Any, value: Any) -> None:
        setattr(getattr(self, attribute_name), property_name, value)

    return property(getter, setter)


class Buffer:
    def __init__(self, data: str) -> None:
        self.data = [list(line) if line else [''] for line in data.split("\n")]
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
    def __init__(self, top: int = 0, lines: int = 5, columns: int = 80) -> None:
        self.top = top
        self.lines = lines
        self.columns = columns


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
        web_mode: bool = False,
    ) -> None:
        self._buffer = Buffer(data=data)
        self._cursor = Cursor(row, col, self._buffer)
        self._screen = Screen(top=0, lines=self.length)
        if _is_out_of_bounds(self):
            raise ValueError("Cursor out of bounds")

        self.mode = "x"  ## x: normal, i: insert, v: visual, r: replace, c: command
        self.web_mode = web_mode

        if params is None:
            params = {}

        self.verbose = params.get("verbose", True)
        self.gif = params.get("gif", False)
        self.sleep_time = params.get("sleep_time", 1)
        self.file_path: str = str(params.get("file_path", "output.txt"))
        self._cmd: list[str] = []

    width = delegate_property("_buffer", "width")
    length = delegate_property("_buffer", "length")
    row = delegate_property("_cursor", "row")
    col = delegate_property("_cursor", "col")
    buffer = delegate_property("_buffer", "data")

    def __getitem__(self, key: int) -> list[str]:
        return self._buffer.data[key]

    def __setitem__(self, key: int, value: list[str]) -> None:
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
            ret, _ = self.exec(command)
            if ret:
                command = ""
            elif command.endswith("<Esc>"):
                command = ""

    """
    Return a tuple of (bool, str).
    bool: True if the command is executed, False if the command is not executed.
    str: The output of the command for web mode.
    """

    def exec(self, commands: str) -> Tuple[bool, str]:
        output = _print(self, commands, (0, 0))

        index = 0
        while index < len(commands):
            command, new_index = self.match(commands[index:])
            if command:
                command(self, commands[index : index + new_index])
                if self.verbose:
                    _update_screen(self)
                    output = _print(self, commands, (index, index + new_index))
                    if self.gif and not self.web_mode:
                        sleep(self.sleep_time)
                self._cmd.append(commands[index : index + new_index])
                index += new_index
            else:
                return False, output
        return True, output

    def match(self, commands: str) -> Tuple[Optional[Callable], int]:
        for pattern, command in match_table[self.mode].items():
            result = re.search("^" + pattern, commands)
            if result:
                return command, result.end()
        return None, 0

    @staticmethod
    def print_keybindings() -> None:
        """Print all supported keystrokes for each mode."""
        print("PyVim Supported Keystrokes")
        print("=" * 50)
        
        mode_names = {
            "x": "NORMAL mode",
            "i": "INSERT mode", 
            "c": "COMMAND mode",
            "r": "REPLACE mode"
        }
        
        for mode, mode_name in mode_names.items():
            print(f"\n{mode_name}:")
            print("-" * len(mode_name))
            
            for pattern, func in sorted(match_table[mode].items()):
                # Extract keystroke from function name
                func_name = func.__name__
                if func_name.startswith("operator_"):
                    key = func_name[9:]  # Remove "operator_" prefix
                elif func_name.startswith("motion_"):
                    key = func_name[7:]  # Remove "motion_" prefix
                else:
                    key = func_name
                
                # Format special keys
                key = key.replace("_", " ")
                key = key.replace("esc", "Esc")
                key = key.replace("enter", "Enter")
                key = key.replace("tab", "Tab")
                key = key.replace("ctrl c", "Ctrl+C")
                key = key.replace("colon", ":")
                key = key.replace("dollar", "$")
                key = key.replace("caret", "^")
                key = key.replace("num ", "{N}")
                key = key.replace("char", "{char}")
                
                print(f"  {key}: {pattern}")
    
    def __del__(self) -> None:
        print("\n\n")
