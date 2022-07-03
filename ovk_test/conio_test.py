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
        print("Premi 'q' per uscire")
        do_quit = False
        while not do_quit:
            while not self.console.is_kbhit():
                pass
            ch = self.console.get_char()
            if ch == 27:
                a = self.console.read_line()
                print(f"\nHai premuto {ord(ch)} {ord(a)} ")
            else:
                self.console.putch(ch)
            print(f"\nHei, hai premuto '{ch}' -> {ord(ch)}")
            if ch == 'q':
                do_quit = True
        print("Bene, ciao")
        ...


# the_test = ConioConsoleTest()
# the_test.print_info()
# the_test.run_test()
