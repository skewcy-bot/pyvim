"""
Author: <Chuanyu> (skewcy@gmail.com)
edit.py (c) 2024
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


def edit_esc(vim: VimEmulator, args: str = "") -> VimEmulator:
    vim.mode = "x"
    return vim


match_table["\<esc\>"] = edit_esc


"""
Insert to buffer.

!!!!!! Make sure this is the last item in match_table. !!!!!!!
"""


def edit_input(vim: VimEmulator, args: str = "") -> VimEmulator:
    assert len(args) == 1

    vim.buffer[vim.row] = (
        vim.buffer[vim.row][: vim.col] + [args] + vim.buffer[vim.row][vim.col :]
    )

    vim.col += 1
    return vim


match_table["."] = edit_input
