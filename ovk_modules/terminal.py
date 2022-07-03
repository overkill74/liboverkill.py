import ovk_modules

from ovk_modules.conio import *


class OvkTerminal:
    """ The terminal class """

    def __init__(self, cmd_list: list[dict]):
        self.conio = ovk_modules.conio.ConioConsole()
        self.command = ""
        self.prompt = ">> "
        self.must_prompt = True
        self.command_list = cmd_list

    def do_prompt(self):
        self.conio.write_str(self.prompt)

    def exec_command(self) -> bool:
        rv = True
        if self.must_prompt:
            # write prompt
            self.must_prompt = False
            self.do_prompt()

        while self.conio.is_kbhit():
            ch = self.conio.get_char()
            self.conio.put_char(ch)
            if ch == "\n":
                # End of line
                if self.command.lower() == "quit":
                    # Quit command
                    rv = False
                elif self.command.lower() == "help":
                    # Help command
                    for it in self.command_list:
                        lcmd = it.get('cmd')
                        while len(lcmd) < 10:
                            lcmd += ' '
                        desc = it.get('desc')
                        print(f"{lcmd} : {desc}")
                else:
                    # search and execute command
                    cmd_found = False
                    for it in self.command_list:
                        lcmd = it.get('cmd').lower()
                        if self.command.lower() == lcmd:
                            print(f"Executing command: {lcmd}")
                            cmd_found = True
                            exefun = it.get('exe')
                            if exefun is None:
                                print("Missing exec function")
                            else:
                                exe_res = exefun()
                                if exe_res == 0:
                                    print("000 OK")
                                else:
                                    print(f"000 FAIL ({exe_res})")
                            break
                    if not cmd_found:
                        print(f"Unknown command {self.command}")

                self.command = ""
                self.must_prompt = True
            else:
                self.command += ch

        return rv
