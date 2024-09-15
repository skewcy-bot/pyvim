"""
Author: <Chuanyu> (skewcy@gmail.com)
edit.py (c) 2024
Desc: description
Created:  2024-09-15T01:40:01.734Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Callable

if TYPE_CHECKING:
    from ..pyvim import VimEmulator

match_table: Dict[str, Callable] = {}


"""
Change to INSERT mode.
"""


def edit_i(vim: VimEmulator, args: str = "") -> VimEmulator:
    vim.mode = "i"
    return vim


match_table["i"] = edit_i


# def edit_R(vim: VimEmulator, args: str = "") -> VimEmulator:
#     vim.mode = "r"
#     return vim
#
#
# def edit_v(vim: VimEmulator, args: str = "") -> VimEmulator:
#     vim.mode = "v"
#     return vim
