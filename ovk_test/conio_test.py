import os
import ovk_modules.conio


class ConioConsoleTest:
    """ The console test """

    def __init__(self) -> object:
        self.console = ovk_modules.conio.ConioConsole()
        pass

    def print_info(self):
        """ Som prints """
        print(f'Running on: {os.name}')
        ...

    def run_test(self):
        """ The console test """
        print("Premi un tasto per uscire")
        while not self.console.is_kbhit():
            pass
        ch = self.console.get_char()
        self.console.put_ch(ch)
        print(f"\nHei, hai premuto '{ch}'")
        print("Bene, ciao")
        ...


# the_test = ConioConsoleTest()
# the_test.print_info()
# the_test.run_test()

"""

Skip to content
All gists
Back to GitHub
@overkill74
@michelbl
michelbl/kbhit.py
Last active 20 days ago • Report abuse

0

    0

Code
Revisions 2
kbhit.py
#!/usr/bin/env python
'''
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
with IDLE.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

import os

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select


class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

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
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        else:
            return sys.stdin.read(1)


    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []


# Test    
if __name__ == "__main__":

    kb = KBHit()

    print('Hit any key, or ESC to exit')

    while True:

        if kb.kbhit():
            c = kb.getch()
            c_ord = ord(c)
            print(c)
            print(c_ord)
            if c_ord == 27: # ESC
                break
            print(c)

    kb.set_normal_term()
@morin-zoom
morin-zoom commented on Feb 16, 2021 •

this doesn't work in python 3
windows10 understands unicode quite well, so you can use msvcrt.getwch
a small example

# coding: utf-8
import msvcrt


while True:
    while msvcrt.kbhit():
        key_in = msvcrt.getwch()
        #arrows, function keys, and so on
        if key_in.encode() == b'\xc3\xa0' or key_in.encode() == b'\x00':
            print(key_in.encode(), end='')
            key_in = msvcrt.getwch()
        #________________________________
        print(key_in.encode())
        print(key_in)
        print('_____')

@ConaII
ConaII commented 20 days ago •

Thanks a lottt, i modified it a little bit:

import os, sys
if os.name == 'nt':
    import msvcrt
else:
    import termios
    import atexit
    from select import select

class lxTerm:
    def start(self, perform=True):
        if os.name != 'nt' and perform:
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)
            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
            # Support normal-terminal reset at exit
            atexit.register(self.reset)

    def reset(self, perform=True):
        if os.name != 'nt' and perform:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self, auto=False):
        self.start(auto)
        if os.name == 'nt':
            x = msvcrt.getch()
        else:
            x = sys.stdin.read(1)
        self.reset(auto)
        return x

    def kbhit(self):
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []

@ConaII
ConaII commented 20 days ago •

example here:

import sys, time

lx = lxTerm()

def main():
    global lx
    print("Press any key to restart the game.")
    lx.getch(True) # Standar getch, no manual needed.

    lx.start() # This will need new term
    while True:
        if lx.kbhit():
            c = lx.getch()
            c_ord = ord(c)
            print(c)
            if c_ord == 27: # ESC
                break
    lx.reset() # Reset to old term

if __name__ == "__main__":
    main()

@overkill74
Attach files by dragging & dropping, selecting or pasting them.
Footer
© 2022 GitHub, Inc.
Footer navigation

    Terms
    Privacy
    Security
    Status
    Docs
    Contact GitHub
    Pricing
    API
    Training
    Blog
    About

You have no unread notifications

"""