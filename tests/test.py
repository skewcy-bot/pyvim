"""
Author: <Chuanyu> (skewcy@gmail.com)
test.py (c) 2024
Desc: description
Created:  2024-07-21T18:28:43.626Z
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from vim_emulator import VimEmulator

import subprocess
import time


class VimSubprocessEmulator:
    def __init__(self, data: str):
        self.filename = "_swap.txt"
        with open(self.filename, "w") as f:
            f.write(data)

        self.process = subprocess.Popen(
            ["vim", "-u", "NONE", "-i", "NONE", "-n", self.filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        time.sleep(0.5)  # Give Vim more time to start up

    def exec(self, commands: str) -> bool:
        for command in commands:
            self.process.stdin.write(command)
        self.process.stdin.flush()
        time.sleep(0.5)  # Increased delay between commands
        return True

    def get_buffer_content(self) -> str:
        self.process.stdin.write(":w\n")  # Save after each command sequence
        self.process.stdin.flush()
        time.sleep(0.5)
        with open(self.filename, "r") as f:
            return f.read()

    # def get_cursor_position(self) -> tuple:
    #     self.process.stdin.write(':echo getpos(".")\n\n')
    #     self.process.stdin.flush()
    #     time.sleep(0.5)
    #     while True:
    #         line = self.process.stdout.readline()
    #         # print(line)
    #         if "[0" in line or "0]" in line:
    #             position = re.findall(r"\d+", line)
    #             break
    #     return position[1], position[2]

    def print(self) -> None:
        # cursor_position = self.get_cursor_position()
        # print(cursor_position)

        content = self.get_buffer_content()
        print(content)

        print("-" * max(len(line) for line in content.split("\n")))

    def __del__(self):
        self.exec(":q!\n")  # Quit Vim without saving
        time.sleep(0.1)
        self.process.terminate()
        time.sleep(0.1)
        # os.remove(self.filename)


# Example usage:
if __name__ == "__main__":
    initial_data = "hello\nworld\nhahahahaha"
    emulator = VimSubprocessEmulator(initial_data)

    emulator.print()
    emulator.exec("Go")  # Go to end of file and enter insert mode
    emulator.exec("New line at the bottom")
    emulator.exec("\x1b")  # Exit insert mode (ESC key)
    emulator.print()
