"""
Author: <Chuanyu> (skewcy@gmail.com)
comms.py (c) 2024
Desc: description
Created:  2024-08-18T19:07:50.750Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple, List, Dict
import sys, tty, os, termios
import copy
import re

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

SPECIAL_CHARS_STR = "~!@#$%^&*()-=+[{]};:'\"\\|,<.>/?"


def _is_spec(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if _is_out_of_bounds(vim, cursor):
        return False
    return vim[cursor.row][cursor.col] in SPECIAL_CHARS_STR


"""
Check if the current character is a word character.
"""


def _is_char(vim: VimEmulator, cursor: Optional[Cursor] = None) -> bool:
    if cursor is None:
        cursor = vim._cursor
    if _is_out_of_bounds(vim, cursor):
        return False

    _is_char = _is_normal(vim, cursor) or _is_spec(vim, cursor)
    _is_space = vim[cursor.row][cursor.col] in [" ", "\t"]
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
    return bool(cursor.col == vim.width[cursor.row] - 1)


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
    if all(char in [" ", "\t"] for char in vim[cursor.row]):
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


def _update_screen(vim: VimEmulator) -> None:
    ## //TODO: Check screen size from terminal size

    vim._screen.lines = vim.length
    vim._screen.columns = max(x for x in vim.width) + 1

    if vim.row < vim._screen.top:
        vim._screen.top = vim.row
    if vim.row >= vim._screen.top + vim._screen.lines:
        vim._screen.top = vim.row - vim._screen.lines + 1


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


def ansi_to_html(text: str) -> str:
    ansi_color_codes = {
        "30": "color:black;",
        "31": "color:red;",
        "32": "color:green;",
        "33": "color:orange;",  # Changed from yellow to orange
        "34": "color:blue;",
        "35": "color:magenta;",
        "36": "color:cyan;",
        "37": "color:white;",
        "40": "background-color:rgba(0,0,0,0.5);",
        "41": "background-color:rgba(255,0,0,0.5);",
        "42": "background-color:rgba(0,255,0,0.5);",
        "43": "background-color:rgba(255,255,0,0.5);",
        "44": "background-color:rgba(0,0,255,0.5);",
        "45": "background-color:rgba(255,0,255,0.5);",
        "46": "background-color:rgba(0,255,255,0.5);",
        "47": "background-color:rgba(255,255,255,0.5);",
        "90": "color:gray;",
        "91": "color:orange;",
        "92": "color:lightgreen;",
        "93": "color:grey;",
        "94": "color:lightblue;",
        "95": "color:lightmagenta;",
        "96": "color:lightcyan;",
        "97": "color:white;",
    }

    def replace_color(match: re.Match[str]) -> str:
        codes = match.group(1).split(";")
        styles = []
        for code in codes:
            if code in ansi_color_codes:
                styles.append(ansi_color_codes[code])
        if styles:
            return f'<span style="{" ".join(styles)}">'
        elif "0" in codes:
            return "</span>"
        return ""

    # Replace color codes
    text = re.sub(r"\033\[([0-9;]+)m", replace_color, text)

    # Replace newlines with <br> tags
    text = text.replace("\n", "<br>")

    # Remove any remaining ANSI escape sequences
    text = re.sub(r"\033\[[0-9;]*[a-zA-Z]", "", text)

    # Ensure all spans are closed
    text += "</span>" * (text.count("<span") - text.count("</span>"))

    return text


def _print(
    vim: VimEmulator, cl: str, comm_range: Tuple[int, int], cursor: bool = True
) -> str:
    _comm = (
        cl[: comm_range[0]]
        + bcolors.FAIL
        + cl[comm_range[0] : comm_range[1]]
        + bcolors.ENDC
        + cl[comm_range[1] :]
    )

    _msg = copy.deepcopy(vim._buffer)

    ## Set cursor color
    if cursor and (vim.mode == "x" or vim.mode == "i" or vim.mode == "r"):
        if vim.mode == "x":
            _cursor_color = 4  # blue
        elif vim.mode == "i":
            _cursor_color = 2  # green
        elif vim.mode == "r":
            _cursor_color = 1  # red
        else:
            _cursor_color = 4  # default to blue
        if vim.row < len(_msg.data) and vim._cursor.col < len(_msg.data[vim.row]):
            char = _msg.data[vim.row][vim._cursor.col]
            _msg.data[vim.row][
                vim._cursor.col
            ] = f"\033[34;4{_cursor_color}m{char}\033[0m"
        elif vim.width[vim.row] == 0:
            _msg.data[vim.row] = [f"\033[34;4{_cursor_color}m \033[0m"]
        elif vim.col >= vim.width[vim.row]:
            _msg.data[vim.row].append(f"\033[34;4{_cursor_color}m \033[0m")
        else:
            assert False, "Invalid cursor position"

    if vim.mode == "x":
        _split_line_color = bcolors.OKBLUE
    elif vim.mode == "i":
        _split_line_color = bcolors.OKGREEN
    elif vim.mode == "c":
        _split_line_color = bcolors.WARNING
    else:
        _split_line_color = bcolors.OKCYAN

    _line_number_width = len(str(vim._screen.top + vim._screen.lines))
    _split = (
        _split_line_color
        + "-" * (max([len(line) for line in _msg.data]) + _line_number_width + 1)
        + bcolors.ENDC
    )
    if vim.gif:
        print(chr(27) + "[2J")

    output = ""
    output += f"Exec: {_comm}\n"
    output += _split + "\n"

    for _line_index in range(
        vim._screen.top, min(vim._screen.top + vim._screen.lines, len(_msg.data))
    ):
        output += (
            bcolors.WARNING
            + str(_line_index + 1)
            + " " * (_line_number_width - len(str(_line_index)))
            + bcolors.ENDC
        )
        output += "".join(_msg.data[_line_index]) + "\n"
    output += _split + "\n"
    output += f"mode: {vim.mode}, cursor: {vim.row},{vim.col}\n"

    if vim.web_mode:
        return ansi_to_html(output)
    else:
        print(output)
        return ""


def _save(vim: VimEmulator, file_path: str) -> None:
    with open(file_path, "w") as f:
        f.write(str(vim._buffer))


def _load(vim: VimEmulator, file_path: str) -> None:
    with open(file_path, "r") as f:
        vim._buffer = Buffer(f.read())


def _get_key() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key_sequence = []

        while True:
            char_bytes = os.read(fd, 1)
            if not char_bytes:
                break
            key_sequence.append(char_bytes)
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
            ch_int: int = key_bytes[0]
            # Control characters (ASCII control codes)
            if ch_int < 32 or ch_int == 127:
                control_mappings: Dict[int, str] = {
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
                return control_mappings.get(ch_int, "<Unknown>")
            else:
                return chr(ch_int)
        else:
            return "<Unknown>"
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# Example usage
if __name__ == "__main__":
    try:
        print("Press keys (Press <Esc> to exit):")
        while True:
            key = _get_key()
            print(f"You pressed: {key}")
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting.")
