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
    _save(vim, vim.file_path)
    vim.mode = "NORMAL"
    return vim


match_table["w\!?<CR>"] = operator_w

"""
Quit
"""


def operator_q(vim: VimEmulator, args: str = "") -> VimEmulator:
    exit(0)


match_table["q\!?<CR>"] = operator_q

"""
Save and quit
"""


def operator_wq(vim: VimEmulator, args: str = "") -> VimEmulator:
    _save(vim, vim.file_path)
    vim.mode = "NORMAL"
    exit(0)


match_table["wq\!?<CR>"] = operator_wq
