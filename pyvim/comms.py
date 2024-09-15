"""
Author: <Chuanyu> (skewcy@gmail.com)
comms.py (c) 2024
Desc: description
Created:  2024-08-18T19:07:50.750Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple, List
import sys, tty, os, termios

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


def get_key() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key_sequence = []

        while True:
            ch = os.read(fd, 1)
            if not ch:
                break
            key_sequence.append(ch)
            break

        key_bytes = b"".join(key_sequence)

        key_mappings = {
            # Arrow keys
            b"\x1b[A": "<Up>",
            b"\x1b[B": "<Down>",
            b"\x1b[C": "<Right>",
            b"\x1b[D": "<Left>",
            # Shift + Arrow keys
            b"\x1b[1;2A": "<S-Up>",
            b"\x1b[1;2B": "<S-Down>",
            b"\x1b[1;2C": "<S-Right>",
            b"\x1b[1;2D": "<S-Left>",
            # Control + Arrow keys
            b"\x1b[1;5A": "<C-Up>",
            b"\x1b[1;5B": "<C-Down>",
            b"\x1b[1;5C": "<C-Right>",
            b"\x1b[1;5D": "<C-Left>",
            # Function keys F1-F12
            b"\x1bOP": "<F1>",
            b"\x1bOQ": "<F2>",
            b"\x1bOR": "<F3>",
            b"\x1bOS": "<F4>",
            b"\x1b[15~": "<F5>",
            b"\x1b[17~": "<F6>",
            b"\x1b[18~": "<F7>",
            b"\x1b[19~": "<F8>",
            b"\x1b[20~": "<F9>",
            b"\x1b[21~": "<F10>",
            b"\x1b[23~": "<F11>",
            b"\x1b[24~": "<F12>",
            # Home, End, Insert, Delete, Page Up, Page Down
            b"\x1b[H": "<Home>",
            b"\x1b[F": "<End>",
            b"\x1b[2~": "<Insert>",
            b"\x1b[3~": "<Del>",
            b"\x1b[5~": "<PageUp>",
            b"\x1b[6~": "<PageDown>",
            # Tab and Backspace
            b"\x7f": "<BS>",
            b"\t": "<Tab>",
            # Escape
            b"\x1b": "<Esc>",
            # Enter
            b"\r": "<CR>",
            b"\n": "<NL>",
            # Space
            b" ": "<Space>",
        }

        # Check if the key sequence matches any in the key_mappings
        if key_bytes in key_mappings:
            return key_mappings[key_bytes]
        elif key_bytes.startswith(b"\x1b"):
            # Possible Alt/Meta key combinations
            if len(key_bytes) == 2:
                return f"<M-{chr(key_bytes[1])}>"
            else:
                # Handle other special cases if needed
                return "<Unknown>"
        elif len(key_bytes) == 1:
            ch = key_bytes[0]
            # Control characters (ASCII control codes)
            if ch < 32 or ch == 127:
                control_mappings = {
                    0: "<Nul>",
                    1: "<C-A>",
                    2: "<C-B>",
                    3: "<C-C>",
                    4: "<C-D>",
                    5: "<C-E>",
                    6: "<C-F>",
                    7: "<C-G>",
                    8: "<BS>",
                    9: "<Tab>",
                    10: "<NL>",
                    11: "<C-K>",
                    12: "<C-L>",
                    13: "<CR>",
                    14: "<C-N>",
                    15: "<C-O>",
                    16: "<C-P>",
                    17: "<C-Q>",
                    18: "<C-R>",
                    19: "<C-S>",
                    20: "<C-T>",
                    21: "<C-U>",
                    22: "<C-V>",
                    23: "<C-W>",
                    24: "<C-X>",
                    25: "<C-Y>",
                    26: "<C-Z>",
                    27: "<Esc>",
                    28: "<C-\>",
                    29: "<C-]>",
                    30: "<C-6>",
                    31: "<C-/>",
                    127: "<Del>",
                }
                return control_mappings.get(ch, "<Unknown>")
            else:
                return chr(ch)
        else:
            return "<Unknown>"
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# Example usage
if __name__ == "__main__":
    try:
        print("Press keys (Press <Esc> to exit):")
        while True:
            key = getkey()
            print(f"You pressed: {key}")
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting.")
