"""
Author: <Chuanyu> (skewcy@gmail.com)
operator.py (c) 2024
Desc: description
Created:  2024-09-15T01:40:01.734Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Callable, List
from ..comms import _is_empty_line

if TYPE_CHECKING:
    from ..pyvim import VimEmulator

match_table: Dict[str, Callable] = {}


"""
Change to INSERT mode.
"""


def operator_i(vim: VimEmulator, args: str = "") -> VimEmulator:
    vim.mode = "i"
    return vim


match_table["i"] = operator_i

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

    if ends_with_space:
        vim[cursor.row] = current_line + lstrip(next_line)
    else:
        vim[cursor.row] = rstrip(current_line) + [" "] + lstrip(next_line)

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

    vim[cursor.row] = vim[cursor.row] + vim[cursor.row + 1]

    vim.width[cursor.row] = len(vim[cursor.row])
    vim.buffer.pop(cursor.row + 1)
    vim.length -= 1
    return vim


match_table["gJ"] = operator_gJ
