"""
Author: <Chuanyu> (skewcy@gmail.com)
main.py (c) 2024
Desc: description
Created:  2024-07-21T16:32:00.918Z
"""

from vim_emulator.pyvim import VimEmulator


if __name__ == "__main__":

    ## //ANCHOR - Test hjkl
    # VimEmulator("hello\nworld\nhahahahaha").exec("")
    # VimEmulator("hello\nworld\nhahahahaha").exec("hjkhlklhkjhjlkhkjhjhjhlj")

    ## //ANCHOR - Test w
    # VimEmulator("hello world hahahahaha").exec("w")
    # VimEmulator("hello world hahahahaha").exec("ww")
    # VimEmulator("hello world hahahahaha").exec("www")
    # VimEmulator("hello world\n hahahahaha").exec("www")
    # VimEmulator("hello world\n\n\n hahahahaha").exec("www")
    # VimEmulator("hello world\n\n\n hahahahaha").exec("wwww")
    # VimEmulator("hello $orld\n\n\n hahahahaha").exec("wwww")
    # VimEmulator("hello w$rld\n\n\n hahahahaha").exec("wwwwwwww")

    ## //ANCHOR - Test W
    # VimEmulator("hello w$rld\n\n\n hahahahaha").exec("WWWWWWWW")

    ## //ANCHOR - Test e
    # VimEmulator("hello world hahahahaha").exec("eee")
    # VimEmulator("hello world\n hahahahaha").exec("eee")
    # VimEmulator("hello world\n\n\n hahahahaha").exec("eee")
    # VimEmulator("hello world\n\n\n hahahahaha").exec("eeee")
    # VimEmulator("hello $orld\n\n\n hahahahaha").exec("eeee")
    # VimEmulator("hello w$rld\n\n\n hahahahaha").exec("eeeeeeee")

    ## //ANCHOR - Test E
    VimEmulator("hello w$rld\n\n\n hahahahaha").exec("EEEEEEEEEE")
