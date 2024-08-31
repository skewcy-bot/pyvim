"""
Author: <Chuanyu> (skewcy@gmail.com)
operators.py (c) 2024
Desc: description
Created:  2024-07-21T17:28:49.755Z
"""

from __future__ import annotations
from copy import deepcopy
from typing import TYPE_CHECKING, Dict, Callable

from ..comms import (
    _is_out_of_bounds,
    _is_word_start,
    _is_Word_start,
    _is_word_end,
    _is_Word_end,
    _is_empty_line,
    _is_blank_line,
)

if TYPE_CHECKING:
    from ..pyvim import VimEmulator


"""
Match table for NORMAL commands in REGEX.
"""
match_table: Dict[str, Callable] = {}


def motion_l(vim: VimEmulator) -> VimEmulator:
    vim.col = min(vim.col + 1, vim.width[vim.row] - 1)
    return vim


match_table["l"] = motion_l


def motion_k(vim: VimEmulator) -> VimEmulator:
    vim.row = max(0, vim.row - 1)
    return vim


match_table["k"] = motion_k


def motion_j(vim: VimEmulator) -> VimEmulator:
    vim.row = min(vim.row + 1, vim.length - 1)
    return vim


match_table["j"] = motion_j


def motion_h(vim: VimEmulator) -> VimEmulator:
    vim.col = max(0, vim.col - 1)
    return vim


match_table["h"] = motion_h


"""
Move the cursor to the beginning of the next word.

    - Special case: Not find this line, move to the next word on the next line, or the end of this line, or next empty line.
    - Special case: If all characters are non-word characters next line, skip this line.
"""


def motion_w(vim: VimEmulator) -> VimEmulator:
    vim.col += 1
    while not _is_out_of_bounds(vim) and not _is_word_start(vim):
        vim.col += 1

    ## Special case: Not find this line
    if _is_out_of_bounds(vim):
        if vim.row < vim.length - 1:
            vim.row += 1
            vim.col = 0
            while _is_blank_line(vim) and vim.row < vim.length - 1:
                vim.row += 1
                vim.col = 0
            while not _is_out_of_bounds(vim) and not _is_word_start(vim):
                vim.col += 1
        else:
            vim.col = min(vim.col, vim.width[vim.row] - 1)
    return vim


match_table["w"] = motion_w


"""
Move the cursor to the beginning of the next WORD.

    - Special case: Not find this line, move to the next word on the next line, or the end of this line, or next empty line.
"""


def motion_W(vim: VimEmulator) -> VimEmulator:
    vim.col += 1
    while not _is_out_of_bounds(vim) and not _is_Word_start(vim):
        vim.col += 1

    ## Special case: Not find this line
    if _is_out_of_bounds(vim):
        if vim.row < vim.length - 1:
            vim.row += 1
            vim.col = 0
            while _is_blank_line(vim) and vim.row < vim.length - 1:
                vim.row += 1
                vim.col = 0
            while not _is_out_of_bounds(vim) and not _is_Word_start(vim):
                vim.col += 1
        else:
            vim.col = min(vim.col, vim.width[vim.row] - 1)
    return vim


match_table["W"] = motion_W

"""
Move the cursor to the end of the next word.

    - Special case: Not find this line, move to the next word on the next line, or the end of this line.
    - Special case: It skip next line if it is empty.
"""


def motion_e(vim: VimEmulator) -> VimEmulator:
    vim.col += 1
    while not _is_out_of_bounds(vim) and not _is_word_end(vim):
        vim.col += 1

    ## Special case: Not find this line
    if _is_out_of_bounds(vim):
        ## Next line exists
        if vim.row < vim.length - 1:
            vim.row += 1
            vim.col = 0
            ## Skip empty line
            while _is_empty_line(vim) and vim.row < vim.length - 1:
                vim.row += 1
                vim.col = 0
            while not _is_out_of_bounds(vim) and not _is_word_end(vim):
                vim.col += 1
        else:
            vim.col = min(vim.col, vim.width[vim.row] - 1)
    return vim


match_table["e"] = motion_e

"""
Move the cursor to the end of the next WORD.

    - Special case: Not find this line, move to the next word on the next line, or the end of this line.
    - Special case: It skip next line if it is empty.
"""


def motion_E(vim: VimEmulator) -> VimEmulator:
    vim.col += 1
    while not _is_out_of_bounds(vim) and not _is_Word_end(vim):
        vim.col += 1

    ## Special case: Not find this line
    if _is_out_of_bounds(vim):
        ## Next line exists
        if vim.row < vim.length - 1:
            vim.row += 1
            vim.col = 0
            ## Skip empty line
            while _is_empty_line(vim) and vim.row < vim.length - 1:
                vim.row += 1
                vim.col = 0
            while not _is_out_of_bounds(vim) and not _is_Word_end(vim):
                vim.col += 1
        else:
            vim.col = min(vim.col, vim.width[vim.row] - 1)
    return vim


match_table["E"] = motion_E

"""
Move the cursor to the start of previous word.

    - Special case: Not find this line, move to the previous word on the previous line, or the start of this line.
    - Special case: It skip previous line if it is empty.
"""


def motion_b(vim: VimEmulator) -> VimEmulator:
    vim.col -= 1
    while not _is_out_of_bounds(vim) and not _is_word_start(vim):
        vim.col -= 1

    ## Special case: Not find this line
    if _is_out_of_bounds(vim):
        if vim.row > 0:
            vim.row -= 1
            vim.col = vim.width[vim.row] - 1
            while _is_blank_line(vim) and vim.row > 0:
                vim.row -= 1
                vim.col = vim.width[vim.row] - 1
            while not _is_out_of_bounds(vim) and not _is_word_start(vim):
                vim.col -= 1
        else:
            vim.col = max(vim.col, 0)
    return vim


match_table["b"] = motion_b


"""
Move the cursor to the start of previous WORD.
    
        - Special case: Not find this line, move to the previous word on the previous line, or the start of this line.
        - Special case: It skip previous line if it is empty.
"""


def motion_B(vim: VimEmulator) -> VimEmulator:
    vim.col -= 1
    while not _is_out_of_bounds(vim) and not _is_Word_start(vim):
        vim.col -= 1

    ## Special case: Not find this line
    if _is_out_of_bounds(vim):
        if vim.row > 0:
            vim.row -= 1
            vim.col = vim.width[vim.row] - 1
            while _is_blank_line(vim) and vim.row > 0:
                vim.row -= 1
                vim.col = vim.width[vim.row] - 1
            while not _is_out_of_bounds(vim) and not _is_Word_start(vim):
                vim.col -= 1
        else:
            vim.col = max(vim.col, 0)
    return vim


match_table["B"] = motion_B

"""
Move the cursor to the first non-blank character of the line.
"""


def motion_caret(vim: VimEmulator) -> VimEmulator:
    if _is_empty_line(vim):
        return vim
    vim.col = 0
    while not _is_out_of_bounds(vim) and vim[vim.row][vim.col] == " ":
        vim.col += 1
    if _is_out_of_bounds(vim):
        vim.col = vim.width[vim.row] - 1
    return vim


match_table["\^"] = motion_caret


"""
Move the cursor to the end of the line.
"""


def motion_dollar(vim: VimEmulator) -> VimEmulator:
    if _is_empty_line(vim):
        return vim
    vim.col = vim.width[vim.row] - 1
    return vim


match_table["\$"] = motion_dollar

"""
Move the cursor to the start of the line. 
"""


def motion_zero(vim: VimEmulator) -> VimEmulator:
    if _is_empty_line(vim):
        return vim
    vim.col = 0
    return vim


match_table["0"] = motion_zero


"""
Move the cursor to the top of the screen.
"""


def motion_H(vim: VimEmulator) -> VimEmulator:
    vim.row = vim._screen.top
    if _is_empty_line(vim) or _is_blank_line(vim):
        vim.col = 0
    else:
        motion_caret(vim)
    return vim


match_table["H"] = motion_H

"""
Move the cursor to the middle of the line.
"""


def motion_M(vim: VimEmulator) -> VimEmulator:
    vim.row = vim._screen.top + vim._screen.lines // 2
    if _is_empty_line(vim) or _is_blank_line(vim):
        vim.col = 0
    else:
        motion_caret(vim)
    return vim


match_table["M"] = motion_M

"""
Move the cursor to the bottom of the line.
"""


def motion_L(vim: VimEmulator) -> VimEmulator:
    vim.row = vim._screen.top + vim._screen.lines - 1
    if _is_empty_line(vim) or _is_blank_line(vim):
        vim.col = 0
    else:
        motion_caret(vim)
    return vim


match_table["L"] = motion_L

"""
Move cursor to the paired bracket.
"""


def motion_percent(vim: VimEmulator) -> VimEmulator:
    _paired_brackets = {"(": ")", "{": "}", "[": "]", ")": "(", "}": "{", "]": "["}
    _forward_brackets = set(["(", "{", "["])

    if vim[vim.row][vim.col] in _forward_brackets:
        ## Search in currrent line
        for i in range(vim.col + 1, vim.width[vim.row]):
            if vim[vim.row][i] == _paired_brackets[vim[vim.row][vim.col]]:
                vim.col = i
                return vim
        ## Search in next lines
        for i in range(vim.row + 1, vim.length):
            for j in range(vim.width[i]):
                if vim[i][j] == _paired_brackets[vim[vim.row][vim.col]]:
                    vim.row = i
                    vim.col = j
                    return vim
    else:
        ## Search in currrent line
        for i in range(vim.col - 1, -1, -1):
            if vim[vim.row][i] == _paired_brackets[vim[vim.row][vim.col]]:
                vim.col = i
                return vim
        ## Search in previous lines
        for i in range(vim.row - 1, -1, -1):
            for j in range(vim.width[i] - 1, -1, -1):
                if vim[i][j] == _paired_brackets[vim[vim.row][vim.col]]:
                    vim.row = i
                    vim.col = j
                    return vim
    return vim


match_table["%"] = motion_percent

"""
Move cursor to next paragraph.

    - If the cursor is on a blank line, move to the next bland line, then move to the next non-blank line. 
    - If the cursor is on a non-blank line, move to the next blank line.
"""


def motion_brace_right(vim: VimEmulator) -> VimEmulator:
    _cursor = deepcopy(vim._cursor)
    vim.row += 1
    # if empty line
    if _is_empty_line(vim, _cursor):
        ## Move to the next non-empty line
        while vim.row < vim.length and _is_empty_line(vim):
            vim.row += 1

    ## Move to the next empty line
    while vim.row < vim.length and not _is_empty_line(vim):
        vim.row += 1

    if vim.row == vim.length:
        vim.row -= 1
        motion_dollar(vim)
    return vim


match_table["\}"] = motion_brace_right

"""
Move cursor to previous paragraph.
"""

def motion_brace_left(vim: VimEmulator) -> VimEmulator:
    _cursor = deepcopy(vim._cursor)
    vim.row -= 1
    # if empty line
    if _is_empty_line(vim, _cursor):
        ## Move to the previous non-empty line
        while vim.row >= 0 and _is_empty_line(vim):
            vim.row -= 1

    ## Move to the previous empty line
    while vim.row >= 0 and not _is_empty_line(vim):
        vim.row -= 1

    if vim.row == -1:
        vim.row += 1
        motion_zero(vim)
    return vim

match_table["\{"] = motion_brace_left
