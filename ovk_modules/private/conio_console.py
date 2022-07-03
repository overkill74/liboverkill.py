"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import os

if os.name == 'nt':  # Windows
    os = 'nt'
    import msvcrt
else:  # Posix (Linux, OS X)
    os = 'LINUX'
    import sys
    import termios
    import atexit
    from select import select

# special key definitions
ENTER = 10
ESC = 27
BACKSPACE = 127
TAB = 9


class ConioConsole():
    """ Conio Console """

    def getch(self):
        BaseException(self)

    def kbhit(self):
        BaseException(self)

    def put_ch(self, ch):
        BaseException(self)


class ConioConsolePosix(ConioConsole):
    def __init__(self):
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """ Resets to normal terminal.  On Windows does nothing """
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self):
        return sys.stdin.read(1)

    def kbhit(self):
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []

    def put_ch(self, ch):
        return sys.stdout.write(ch)


class ConioConsoleWinows(ConioConsole):
    """ this class does the work """

    def getch(self):
        """ Returns a keyboard character after kbhit() has been called """
        return msvcrt.getch().decode('utf-8')

    def kbhit(self):
        return msvcrt.kbhit()

    def put_ch(self, ch):
        return msvcrt.putch(ch)


class ConioConsolleBuilder(ConioConsole):
    @staticmethod
    def create_me() -> object:
        if os == 'nt':
            return ConioConsoleWinows()
        else:
            return ConioConsolePosix()
