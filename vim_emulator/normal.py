"""
Author: <Chuanyu> (skewcy@gmail.com)
operators.py (c) 2024
Desc: description
Created:  2024-07-21T17:28:49.755Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Callable

from .comms import _is_out_of_bounds, _is_word_start, _is_Word_start,_is_word_end, _is_Word_end

if TYPE_CHECKING:
    from .vim_emulator import VimEmulator


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

