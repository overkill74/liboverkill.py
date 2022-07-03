import functools

from ovk_modules.private.conio_console import *


# class Conio():
#     """
#     Conio class declaration
#     This is a pure virtual class
#     """
#
#     def is_kbhit(self):
#         # is_kbhit
#         ...
#
#     def get_char(self):
#         # getCh
#         ...
#
#     def put_ch(self, ch):
#         # putch
#         ...


class ConioConsole(ConioConsole):
    # Conio on Consolle
    kb_hit = ConioConsolleBuilder().create_me()

    def __int__(self) -> object:
        pass

    def is_kbhit(self):
        return self.kb_hit.kbhit()

    def get_char(self):
        return self.kb_hit.getch()

    def put_char(self, ch):
        self.kb_hit.putch(ch)

    def read_line(self) -> str:
        return self.kb_hit.read_line()

    def write_str(self, txt) -> str:
        self.kb_hit.write_str(txt)
