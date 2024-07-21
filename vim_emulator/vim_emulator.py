"""
Author: <Chuanyu> (skewcy@gmail.com)
vim_emulator.py (c) 2024
Desc: description
Created:  2024-07-21T16:32:14.272Z
"""

from typing import Callable, Tuple, Optional
from copy import deepcopy
import re

from .commands import match_table


class Cursor:
    def __init__(self, row: int, col: int) -> None:
        self.x = row
        self.y = col


class Buffer:
    def __init__(self, data: str) -> None:
        self.data = [list(line) for line in data.split("\n")]
        self.width = max(len(line) for line in self.data)
        self.length = len(self.data)

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.data)


class VimEmulator:
    def __init__(self, data: str) -> None:
        self.cursor = Cursor(0, 0)
        self.buffer = Buffer(data=data)

        self.mode = "x"  ## x: normal, i: insert, v: visual, r: replace, c: command

        self.verbose = True

    def exec(self, commands: str) -> bool:
        if self.verbose:
            print(f"Executing: {commands}")
            self.print()

        index = 0
        while index < len(commands):
            command, new_index = self.match(commands[index:])
            if command:
                command(self, *commands[index + 1 : index + new_index])
                if self.verbose:
                    self.print()
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

    def print(self) -> None:
        _msg = deepcopy(self.buffer)
        _msg.data[self.cursor.y][self.cursor.x] = "█"
        print(_msg)
        print("-" * self.buffer.width)
