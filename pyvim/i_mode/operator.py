"""
Author: <Chuanyu> (skewcy@gmail.com)
operator.py (c) 2024
Desc: description
Created:  2024-09-15T01:48:18.019Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Callable

if TYPE_CHECKING:
    from ..pyvim import VimEmulator

match_table: Dict[str, Callable] = {}


"""
Change to NORMAL mode.
"""


def operator_esc(vim: VimEmulator, args: str = "") -> VimEmulator:
    vim.mode = "x"
    return vim


match_table["\<Esc\>"] = operator_esc


"""
New line in INSERT mode.
"""


def operator_enter(vim: VimEmulator, args: str = "") -> VimEmulator:
    new_line = vim.buffer[vim.row][vim.col :]

    vim.buffer[vim.row] = vim.buffer[vim.row][: vim.col]
    vim.width[vim.row] = len(vim.buffer[vim.row])

    vim.length += 1
    vim.buffer.insert(vim.row + 1, new_line)
    vim.width.insert(vim.row + 1, len(new_line))

    vim.row += 1
    vim.col = 0
    return vim


match_table["\<CR\>"] = operator_enter


"""
Handle Tab key in INSERT mode.
"""


def operator_tab(vim: VimEmulator, args: str = "") -> VimEmulator:
    # Insert 4 spaces for tab (or customize as needed)
    for _ in range(4):
        vim.buffer[vim.row] = (
            vim.buffer[vim.row][: vim.col] + [" "] + vim.buffer[vim.row][vim.col :]
        )
        vim.col += 1
        vim.width[vim.row] += 1
    return vim


match_table["\<Tab\>"] = operator_tab


"""
Handle Ctrl+C in INSERT mode (should exit to normal mode or be ignored).
"""


def operator_ctrl_c(vim: VimEmulator, args: str = "") -> VimEmulator:
    # In vim, Ctrl+C in insert mode exits to normal mode
    vim.mode = "x"
    return vim


match_table["\<C-C\>"] = operator_ctrl_c


"""
Insert to buffer.

!!!!!! Make sure this is the last item in match_table. !!!!!!!
"""


def operator_input(vim: VimEmulator, args: str = "") -> VimEmulator:
    assert len(args) == 1

    vim.buffer[vim.row] = (
        vim.buffer[vim.row][: vim.col] + [args] + vim.buffer[vim.row][vim.col :]
    )

    vim.col += 1
    vim.width[vim.row] += 1
    return vim


match_table["."] = operator_input
