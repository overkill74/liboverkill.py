
import os

from ovk_modules.terminal import *


class TerminalTest:
    def __init__(self):
        self.cmd = [
            {'cmd': 'AAA', 'desc': 'COMANDO_A', 'exe': 'self.fun_aaa'},
            {'cmd': 'BBB', 'desc': 'COMANDO_B', 'exe': 'self.fun_bbb'},
            {'cmd': 'CCC', 'desc': 'COMANDO_C', 'exe': 'self.fun_ccc'},
        ]
        self.terminal = OvkTerminal(self.cmd)

    def fun_aaa(self):
        print("I am AAA")

    def fun_bbb(self):
        print("I am BBB")

    def fun_ccc(self):
        print("I am CCC")

    def run_test(self):
        """ The terminal test """
        print("Terminal test")
        do_run = True
        while do_run:
            do_run = self.terminal.exec_command()
        print("Bene, ciao")
