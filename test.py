"""
Author: <Chuanyu> (skewcy@gmail.com)
main.py (c) 2024
Desc: description
Created:  2024-07-21T16:32:00.918Z
"""

from pyvim.pyvim import VimEmulator
from pyvim.comms import _get_random_buffer
from web.web import PyVimWeb

if __name__ == "__main__":
    pass
    ## //ANCHOR - Test hjkl
    # VimEmulator("hello\nworld\nhahahahaha").exec("")
    # VimEmulator("hello\nworld\nhahahahaha").exec("hjkhlklhkjhjlkhkjhjhjhlj")

    # # //ANCHOR - Test w
    # VimEmulator("hello world hahahahaha").exec("w")
    # VimEmulator("hello world hahahahaha").exec("ww")
    # VimEmulator("hello world hahahahaha").exec("www")
    # VimEmulator("hello world\n hahahahaha").exec("www")
    # VimEmulator("hello world\n\n\n hahahahaha").exec("www")
    # VimEmulator("hello world\n\n\n hahahahaha").exec("wwww")
    # VimEmulator("hello $orld\n\n\n hahahahaha").exec("wwww")
    # VimEmulator("hello w$rld\n\n    \n hahahahaha").exec("wwwwwwww")

    # # //ANCHOR - Test W
    # VimEmulator("hello w$rld\n\n    \n hahahahaha").exec("WWWWWWWW")

    ## //ANCHOR - Test e
    # VimEmulator("hello world hahahahaha").exec("eee")
    # VimEmulator("hello world\n hahahahaha").exec("eee")
    # VimEmulator("hello world\n\n\n hahahahaha").exec("eee")
    # VimEmulator("hello world\n\n\n hahahahaha").exec("eeee")
    # VimEmulator("hello $orld\n\n\n hahahahaha").exec("eeee")
    # VimEmulator("hello w$rld\n\n\n hahahahaha").exec("eeeeeeee")

    ## //ANCHOR - Test E
    # VimEmulator("hello w$rld\n\n\n hahahahaha").exec("EEEEEEEEEE")

    # ## //ANCHOR - Test b
    # VimEmulator("hello world hahahahaha", 0, 15).exec("bbbb")
    # VimEmulator("hello w$rld\n\n     \n  hahahahaha", 3, 5).exec("bbbb")

    # ## //ANCHOR - Test LMH
    # VimEmulator(_get_random_buffer(5, 10)).exec("LMHHML")

    # ## //ANCHOR - Test %
    # VimEmulator("hello world\n\n\n hahahahaha").exec("%%")
    # VimEmulator("{hello world\n\n\n hahahahaha}").exec("%%")
    # VimEmulator("{hello (world\n\n\n hahaha}haha)", -1, -1).exec("%%")

    # ## //ANCHOR - Test ^
    # VimEmulator("hello world\n\n\n hahahahaha", 0, 5).exec("^")
    # VimEmulator("hello world\n\n    \n hahahahaha", 0, 0).exec("j^")
    # VimEmulator("hello world\n\n    \n hahahahaha", 2, 1).exec("^")

    ## //ANCHOR - Test $
    # VimEmulator("hello world\n\n\n hahahahaha", 0, 5).exec("$")

    ## //ANCHOR - Test 0
    # VimEmulator("hello world\n\n\n hahahahaha", 0, 5).exec("0")

    ## //ANCHOR - Test }
    # VimEmulator("hello world\n\n    \n hahahahaha", 0, 2).exec("}")
    # VimEmulator("hello world\n    \n hahahahaha\n\n \naasdf\n", 0, 2).exec("}}}")

    ## //ANCHOR - Test {
    # VimEmulator("hello world\n    \n hahahahaha\n\n \naasdf", -1, -1).exec("{{{{")

    ## //ANCHOR - Test ge
    # VimEmulator("hello world\n\n   \n hahahahaha", 0, 5).exec("ge")
    # VimEmulator("hello world\n\n\n   \n hahahahaha", -1, -1).exec("gegege")

    ## //ANCHOR - Test gE
    # VimEmulator("hello world\n\n\n hahahahaha", 0, 5).exec("gE")
    # VimEmulator("hel!!lo wo!!rld\n\n\n   \n ha!!hahahaha", -1, -1).exec("gegEgegEge")

    ## //ANCHOR - Test g_
    # VimEmulator("hello world !!  \n\n\n hahahahaha", 0, 5).exec("g_")

    ## //ANCHOR - Test gg
    # VimEmulator("hello world !!  \n\n\n hahahahaha", -1, 3).exec("gg")

    ## //ANCHOR - Test G
    # VimEmulator("hello world !!  \n\n\n hahahahaha", 0, 3).exec("G")

    ## //ANCHOR - Test \d+gg
    # VimEmulator("hello world !!  \n\n\n hahahahaha", -1, 3).exec("10gg")
    # VimEmulator("hello world !!  \n\n\n hahahahaha", -1, 3).exec("3gg")
    # VimEmulator("hello world !!  \n\n\n hahahahaha", -1, 3).exec("0gg")

    ## //ANCHOR - Test f
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", 0, 0).exec("f f!f ")
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", -1, 0).exec("f f f ")

    ## //ANCHOR - Test F
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", 0, -1).exec("F f!f ")
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", -1, -1).exec("F f f ")

    ## //ANCHOR - Test t
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", 0, 0).exec("t t t ")

    ## //ANCHOR - Test T
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", 0, -1).exec("T!T!T!")

    ## //ANCHOR - Test ;
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", 0, 0).exec("f ;;")
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", 0, -1).exec("F ;;")

    ## //ANCHOR - Test ,
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", 0, 0).exec("F ,,,,")
    # VimEmulator("hello world !!  \n\n\n   hahahahaha", 0, -1).exec("f,,,,")

    ## //ANCHOR - Test z
    # msg = "".join([f"{i}\n" for i in range(10)])
    # VimEmulator(msg, 0, 0).exec("zt")
    # VimEmulator(msg, 0, 0).exec("zz")
    # VimEmulator(msg, 0, 0).exec("zb")

    ## //ANCHOR - Test for insert mode
    # VimEmulator("hello world\n", 0, 0, {"gif": True}).exec("i114514<Esc>0ihaha<Esc>")

    ## //ANCHOR - Test r
    # VimEmulator("hello world\n", 0, 0).exec("r1wr2")

    ## //ANCHOR - Test J
    # VimEmulator("hello  \n world", 0, 0).exec("J")
    # VimEmulator("hello  \nworld", 0, 0).exec("J")
    # VimEmulator("hello \n  world", 0, 0).exec("J")
    # VimEmulator("hello\n  world", 0, 0).exec("J")
    # VimEmulator("hello\nworld", 0, 0).exec("J")
    # VimEmulator("hello\n\nworld", 0, 0).exec("JJ")

    ## //ANCHOR - Test gJ
    # VimEmulator("hello  \n world", 0, 0).exec("gJ")
    # VimEmulator("hello  \nworld", 0, 0).exec("gJ")
    # VimEmulator("hello \n  world", 0, 0).exec("gJ")
    # VimEmulator("hello\n  world", 0, 0).exec("gJ")
    # VimEmulator("hello\nworld", 0, 0).exec("gJ")
    # VimEmulator("hello\n\nworld", 0, 0).exec("gJ")

    ## //ANCHOR - Test \d+\D{1,2}
    # VimEmulator(_get_random_buffer(5, 10), 0, 0).exec("5j5l10ge10gg")

    ## //ANCHOR - Test x
    # VimEmulator("hello world\n", 0, 0).exec("x")
    # VimEmulator("hello world\n", 0, -1).exec("xx")
    # VimEmulator(" ", 0, 0).exec("xxxx")
    # VimEmulator("hello world\n", 0, 0).exec("5x")
    # VimEmulator("a", 0, 0).exec("x")

    ## ========================================
    ## //ANCHOR - Test INTERACTIVE MODE
    # VimEmulator("hello world\n", 0, 0).run()
