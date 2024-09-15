import sys
import tty
import os
import termios

def getkey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        b = os.read(fd, 3)
        if len(b) == 3 and b[0] == '\x1b':  # Escape sequence
            if b[1] == '[':
                key_mapping = {
                    'C': 'right',
                    'D': 'left',
                    'A': 'up',
                    'B': 'down'
                }
                return key_mapping.get(b[2], 'unknown sequence')
        return b.decode()  # Regular characters
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    try:
        while True:
            k = getkey()
            if k == 'esc':
                print('Exiting.')
                break
            else:
                print(f'Key pressed: {k}')
    except KeyboardInterrupt:
        print('Interrupted by user.')
    finally:
        print('Restoring terminal settings.')

if __name__ == "__main__":
    main()
