"""
Author: <Chuanyu> (skewcy@gmail.com)
main.py (c) 2024
Desc: description
Created:  2024-07-21T16:32:00.918Z
"""

from vim_emulator.vim_emulator import VimEmulator


if __name__ == "__main__":

    ## //ANCHOR - Test basic cursor movement
    VimEmulator("hello\nworld\nhahahahaha").exec("")
