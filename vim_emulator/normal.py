"""
Author: <Chuanyu> (skewcy@gmail.com)
operators.py (c) 2024
Desc: description
Created:  2024-07-21T17:28:49.755Z
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .vim_emulator import VimEmulator

match_table = {}


def motion_l(vim: VimEmulator) -> bool:
    vim.cursor.col = min(vim.cursor.col + 1, vim.buffer.width - 1)
    return True


match_table["l"] = motion_l


def motion_k(vim: VimEmulator) -> bool:
    vim.cursor.row = max(0, vim.cursor.row - 1)
    return True


match_table["k"] = motion_k


def motion_j(vim: VimEmulator) -> bool:
    vim.cursor.row = min(vim.cursor.row + 1, vim.buffer.length - 1)
    return True


match_table["j"] = motion_j


def motion_h(vim: VimEmulator) -> bool:
    vim.cursor.col = max(0, vim.cursor.col - 1)
    return True


match_table["h"] = motion_h

def motion_w(vim: VimEmulator) -> bool:
    _cursor = vim.cursor
    


