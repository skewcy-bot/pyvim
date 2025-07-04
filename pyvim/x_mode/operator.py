"""
Author: <Chuanyu> (skewcy@gmail.com)
operator.py (c) 2024
Desc: description
Created:  2024-09-15T01:40:01.734Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Callable, List
from ..comms import _is_empty_line, _is_out_of_bounds

if TYPE_CHECKING:
    from ..pyvim import VimEmulator


match_table: Dict[str, Callable] = {}


"""
Change to INSERT mode from cursor position.
"""


def operator_i(vim: VimEmulator, args: str = "") -> VimEmulator:
    if vim.col > 0:
        vim.col -= 1
    vim.mode = "i"
    return vim


match_table["i"] = operator_i

"""
Change to INSERT mode from next cursor position.
"""


def operator_a(vim: VimEmulator, args: str = "") -> VimEmulator:
    vim.mode = "i"
    return vim


match_table["a"] = operator_a

"""
Change to INSERT mode from start of next line.
"""


def operator_o(vim: VimEmulator, args: str = "") -> VimEmulator:
    vim.buffer = vim.buffer[: vim.row + 1] + [[]] + vim.buffer[vim.row + 1 :]
    vim.length += 1
    vim.width = vim.width[: vim.row + 1] + [0] + vim.width[vim.row + 1 :]

    vim.row += 1
    vim.col = 0

    vim.mode = "i"
    return vim


match_table["o"] = operator_o

"""
Change to INSERT mode from start of previous line.
"""


def operator_O(vim: VimEmulator, args: str = "") -> VimEmulator:
    vim.buffer = vim.buffer[: vim.row] + [[]] + vim.buffer[vim.row :]
    vim.length += 1
    vim.width = vim.width[: vim.row] + [0] + vim.width[vim.row :]

    vim.col = 0
    vim.mode = "i"
    return vim


match_table["O"] = operator_O

"""
Change to INSERT mode from the first non-blank character of the current line.
"""


def operator_I(vim: VimEmulator, args: str = "") -> VimEmulator:
    if _is_empty_line(vim):
        vim.mode = "i"
        return vim
    vim.col = 0
    while not _is_out_of_bounds(vim) and vim[vim.row][vim.col] in [" ", "\t"]:
        vim.col += 1
    if _is_out_of_bounds(vim):
        vim.col = vim.width[vim.row] - 1
    elif vim.col > 0:
        vim.col -= 1
    vim.mode = "i"
    return vim


match_table["I"] = operator_I

"""
Change to INSERT mode from the end of the current line.
"""


def operator_A(vim: VimEmulator, args: str = "") -> VimEmulator:
    if _is_empty_line(vim):
        vim.mode = "i"
        return vim
    vim.col = vim.width[vim.row] - 1
    vim.mode = "i"
    return vim


match_table["A"] = operator_A

"""
Change to COMMAND mode.
"""


def operator_colon(vim: VimEmulator, args: str = "") -> VimEmulator:
    vim.mode = "c"
    return vim


match_table[":"] = operator_colon


# def operator_R(vim: VimEmulator, args: str = "") -> VimEmulator:
#     vim.mode = "r"
#     return vim
#
#
# def operator_v(vim: VimEmulator, args: str = "") -> VimEmulator:
#     vim.mode = "v"
#     return vim


"""
Replace a single character.
"""


def operator_r(vim: VimEmulator, args: str = "") -> VimEmulator:
    replaced_char = args[1]
    if _is_empty_line(vim):
        return vim
    if vim.col >= vim.width[vim.row]:
        vim.col = vim.width[vim.row] - 1
    cursor = vim._cursor
    vim[cursor.row][cursor.col] = replaced_char
    return vim


match_table["r."] = operator_r


"""
Change into REPLACE mode.
"""


def operator_R(vim: VimEmulator, args: str = "") -> VimEmulator:
    if vim.col > 0:
        vim.col -= 1
    vim.mode = "r"
    return vim


match_table["R"] = operator_R


"""
Join lines.
"""


def operator_J(vim: VimEmulator, args: str = "") -> VimEmulator:
    cursor = vim._cursor
    if cursor.row == len(vim.buffer) - 1:
        return vim

    current_line: List[str] = vim[cursor.row]
    next_line: List[str] = vim[cursor.row + 1]

    def rstrip(line: List[str]) -> List[str]:
        return list("".join(line).rstrip())

    def lstrip(line: List[str]) -> List[str]:
        return list("".join(line).lstrip())

    ends_with_space = rstrip(current_line) != current_line
    stripped_next = lstrip(next_line)
    
    if ends_with_space or not stripped_next:
        vim[cursor.row] = current_line + stripped_next
        # When line ends with space, cursor goes to the space position  
        if ends_with_space and stripped_next:
            vim.col = len(current_line)
        else:
            vim.col = len(current_line) - 1
    else:
        vim[cursor.row] = rstrip(current_line) + [" "] + stripped_next
        # Cursor should be at the space position
        vim.col = len(rstrip(current_line))

    vim.width[cursor.row] = len(vim[cursor.row])
    vim.buffer.pop(cursor.row + 1)
    vim.length -= 1
    return vim


match_table["J"] = operator_J

"""
Join lines without modifying space.
"""


def operator_gJ(vim: VimEmulator, args: str = "") -> VimEmulator:
    cursor = vim._cursor
    if cursor.row == len(vim.buffer) - 1:
        return vim

    original_length = len(vim[cursor.row])
    next_line = vim[cursor.row + 1]
    vim[cursor.row] = vim[cursor.row] + next_line
    # Cursor should be at the first character of what was the second line
    # But if the second line was empty, cursor should be at the last character of the first line
    # An empty line is represented as either [] or ['']
    if len(next_line) == 0 or (len(next_line) == 1 and next_line[0] == ''):
        vim.col = original_length - 1
    else:
        vim.col = original_length

    vim.width[cursor.row] = len(vim[cursor.row])
    vim.buffer.pop(cursor.row + 1)
    vim.length -= 1
    return vim


match_table["gJ"] = operator_gJ

"""
Delete the character under the cursor.
"""


def motion_x(vim: VimEmulator, args: str = "") -> VimEmulator:
    if _is_empty_line(vim):
        return vim
    if _is_out_of_bounds(vim):
        return vim

    vim.buffer[vim.row] = (
        vim.buffer[vim.row][: vim.col] + vim.buffer[vim.row][vim.col + 1 :]
    )
    if vim.col == vim.width[vim.row] - 1 and vim.width[vim.row] > 1:
        vim.col -= 1
    vim.width[vim.row] -= 1

    return vim


match_table["x"] = motion_x
