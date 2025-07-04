"""
Author: <Chuanyu> (skewcy@gmail.com)
main.py (c) 2024
Desc: description
Created:  2024-07-21T16:32:00.918Z
"""

from pyvim.pyvim import VimEmulator
import sys
import os
from typing import List

if __name__ == "__main__":
    args: List[str] = sys.argv

    if len(args) > 1 and args[1] == "web":
        from web.web import app, socketio  # type: ignore

        socketio.run(
            app, debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
        )
    else:
        VimEmulator("hello world\n", 0, 0).run()
