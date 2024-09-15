"""
Author: <Chuanyu> (skewcy@gmail.com)
comms.py (c) 2024
Desc: description
Created:  2024-08-18T19:07:50.750Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple, List

if TYPE_CHECKING:
    from .pyvim import VimEmulator, Cursor, Buffer


"""
Check if the cursor is out of bounds. 
"""


def _is_out_of_bounds(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    return (
        cursor.row < 0
        or cursor.row >= vim.length
        or cursor.col < 0
        or cursor.col >= vim.width[cursor.row]
    )


"""
Check if the current character is a normal character.

    - Out of bounds is not considered a word character.
"""


def _is_normal(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if _is_out_of_bounds(vim, cursor):
        return False
    return (
        vim[cursor.row][cursor.col]
        in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    )


"""
Check if the current character is a word character.

    - Out of bounds is not considered a word character.
"""


def _is_spec(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if _is_out_of_bounds(vim, cursor):
        return False
    return vim[cursor.row][cursor.col] in "~!@#$%^&*()-=+[{]};:'\"\\|,<.>/?"


"""
Check if the current character is a word character.
"""


def _is_char(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if _is_out_of_bounds(vim, cursor):
        return False

    _is_char = _is_normal(vim, cursor) or _is_spec(vim, cursor)
    _is_space = vim[cursor.row][cursor.col] == " "
    assert _is_space != _is_char

    return _is_char


"""
Check if the current character is a line start character.

    - Out of bounds is not considered a line start character.
"""


def _is_line_start(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if _is_out_of_bounds(vim, cursor):
        return False
    return cursor.col == 0


"""
Check if the current character is a line end character.

    - Out of bounds is not considered a line end character.
"""


def _is_line_end(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if _is_out_of_bounds(vim, cursor):
        return False
    return cursor.col == vim.width[cursor.row] - 1


"""
Check if the current character is a word start character.

    - If c is a char and c is line start
    - If c is a char and c-1 is not a char
    - If c is a char and either c is a spec or c-1 is a spec
"""


def _is_word_start(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    from .pyvim import Cursor

    if cursor is None:
        cursor = vim._cursor

    if not _is_char(vim, cursor):
        return False
    else:
        if _is_line_start(vim, cursor):
            return True
        if not _is_char(vim, Cursor(cursor.row, cursor.col - 1)):
            return True
        if _is_spec(vim, cursor) != _is_spec(vim, Cursor(cursor.row, cursor.col - 1)):
            return True
        return False


"""
Check if the current character is a WORD start character.

    - If c is a char and c is line start
    - If c is a char and c-1 is not a char
"""


def _is_Word_start(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    from .pyvim import Cursor

    if cursor is None:
        cursor = vim._cursor

    if not _is_char(vim, cursor):
        return False
    else:
        if _is_line_start(vim, cursor):
            return True
        if not _is_char(vim, Cursor(cursor.row, cursor.col - 1)):
            return True
        return False


"""
Check if the current character is a word end character.

    - If c is a char and c is line end
    - If c is a char and c+1 is not a char
    - If either c is a spec or c+1 is a spec
"""


def _is_word_end(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    from .pyvim import Cursor

    if cursor is None:
        cursor = vim._cursor
    if not _is_char(vim, cursor):
        return False
    else:
        if _is_line_end(vim, cursor):
            return True
        if not _is_char(vim, Cursor(cursor.row, cursor.col + 1)):
            return True
        if _is_spec(vim, cursor) != _is_spec(vim, Cursor(cursor.row, cursor.col + 1)):
            return True
        return False


"""
Check if the current character is a WORD end character.

    - If c is a char and c is line end
    - If c is a char and c+1 is not a char
"""


def _is_Word_end(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    from .pyvim import Cursor

    if cursor is None:
        cursor = vim._cursor
    if not _is_char(vim, cursor):
        return False
    else:
        if _is_line_end(vim, cursor):
            return True
        if not _is_char(vim, Cursor(cursor.row, cursor.col + 1)):
            return True
        return False


"""
Check if the current row buffer is empty.
"""


def _is_empty_line(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if vim.width[cursor.row] == 0:
        return True
    return False


"""
Check if the current row buffer contains no words (only spaces).

    - Empty line is not considered a blank line.
"""


def _is_blank_line(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if len(vim[cursor.row]) == 0:
        return False
    if all(char == " " for char in vim[cursor.row]):
        return True
    return False


"""
Generate a random buffer initialization.
"""


def _get_random_buffer(width: int = 15, length: int = 8) -> str:
    import random

    PRINTABLE = [
        x
        for x in (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
            + "~!@#$%^&*()-=+[{]};:'\"\\|,<.>/?"
        )
    ]

    return "".join(
        [
            "".join(
                [random.choice(PRINTABLE) for y in range(random.randint(1, width))]
                + ["\n"]
            )
        ]
        + [
            "".join(
                [random.choice(PRINTABLE) for y in range(random.randint(0, width))]
                + ["\n"]
            )
            for i in range(1, length)
        ]
    )


def _get_last_cmd_by_head(vim: VimEmulator, head_list: List[str]) -> str:
    for i in range(len(vim._cmd) - 1, -1, -1):
        if vim._cmd[i][0] in head_list:
            return vim._cmd[i]
    return ""


def _get_last_cmd_by_tail(vim: VimEmulator, tail_list: List[str]) -> str:
    for i in range(len(vim._cmd) - 1, -1, -1):
        if vim._cmd[i][-1] in tail_list:
            return vim._cmd[i]
    return ""
