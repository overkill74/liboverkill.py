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
    import gnureadline
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

    def putch(self, ch):
        BaseException(self)

    def read_line(self) -> str:
        BaseException(self)

    def write_str(self, txt):
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

    def putch(self, ch):
        sys.stdout.write(ch)

    def read_line(self) -> str:
        return sys.stdin.readline()

    def write_str(self, txt):
        sys.stdout.write(txt)


class ConioConsoleWinows(ConioConsole):
    """ this class does the work """

    def getch(self):
        """ Returns a keyboard character after kbhit() has been called """
        return msvcrt.getch().decode('utf-8')

    def kbhit(self):
        return msvcrt.kbhit()

    def putch(self, ch):
        return msvcrt.putch(ch)

    def read_line(self) -> str:
        rv = ""
        while msvcrt.kbhit():
            rv += msvcrt.getche().decode('utf-8')
        return rv

    def write_str(self, txt):
        for el in txt:
            msvcrt.putch(el)



class ConioConsolleBuilder(ConioConsole):
    @staticmethod
    def create_me() -> object:
        if os == 'nt':
            return ConioConsoleWinows()
        else:
            return ConioConsolePosix()
