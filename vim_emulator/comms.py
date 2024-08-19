"""
Author: <Chuanyu> (skewcy@gmail.com)
comms.py (c) 2024
Desc: description
Created:  2024-08-18T19:07:50.750Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .vim_emulator import VimEmulator, Cursor, Buffer


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
    from .vim_emulator import Cursor

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
Check if the current character is a word end character.

    - If c is a char and c is line end
    - If c is a char and c+1 is not a char
    - If either c is a spec or c+1 is a spec
"""


def _is_word_end(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    from .vim_emulator import Cursor

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
Check if the current row buffer is empty.
"""


def _is_empty_line(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if vim.width[cursor.row] == 0:
        return True
    return False


def _skip_word(vim: VimEmulator, forward: bool) -> VimEmulator:
    while (
        vim.col < vim.width[vim.row]
        and len(vim[vim.row])
        and _is_Word(vim[vim.row][vim.col])
    ):
        vim.col += 1

        if vim.col == vim.width[vim.row]:
            break
        if _is_word(vim[vim.row][vim.col]) != _is_word(vim[vim.row][vim.col - 1]):
            break
    return vim


def _skip_Word(vim: VimEmulator, forward: bool) -> VimEmulator:
    while (
        vim.col < vim.width[vim.row]
        and len(vim[vim.row])
        and _is_Word(vim[vim.row][vim.col])
    ):
        vim.col += 1
    return vim


def _skip_space(vim: VimEmulator, forward: bool) -> VimEmulator:
    while (
        vim.col < vim.width[vim.row]
        and len(vim[vim.row])
        and vim[vim.row][vim.col] == " "
    ):
        vim.col += 1

    return vim


if __name__ == "__main__":
    assert _is_special("\\") == True
    assert _is_special("'") == True
    assert _is_special('"') == True
