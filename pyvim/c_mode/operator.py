"""
Author: <Chuanyu> (skewcy@gmail.com)
operator.py (c) 2024
Desc: description
Created:  2024-09-15T14:35:52.576Z
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Callable
from ..comms import _save

if TYPE_CHECKING:
    from ..pyvim import VimEmulator

match_table: Dict[str, Callable] = {}


"""
Change to NORMAL mode.
"""


def operator_w(vim: VimEmulator, args: str = "") -> VimEmulator:
    if not vim.web_mode:
        _save(vim, vim.file_path)
    vim.mode = "x"
    return vim


match_table["w\!?<CR>"] = operator_w

"""
Quit
"""


def operator_q(vim: VimEmulator, args: str = "") -> VimEmulator:
    if not vim.web_mode:
        exit(0)
    vim.mode = "x"
    return vim


match_table["q\!?<CR>"] = operator_q

"""
Save and quit
"""


def operator_wq(vim: VimEmulator, args: str = "") -> VimEmulator:
    if not vim.web_mode:
        _save(vim, vim.file_path)
        exit(0)
    vim.mode = "x"
    return vim


match_table["wq\!?<CR>"] = operator_wq

"""
Quit command mode.
"""


def operator_esc(vim: VimEmulator, args: str = "") -> VimEmulator:
    vim.mode = "x"
    return vim


match_table[".*<Esc>"] = operator_esc
