from pexpect.popen_spawn import PopenSpawn as Console
from pexpect import TIMEOUT, EOF
from subprocess import TimeoutExpired
from re import findall


class SafeConsole(Console):
    def kill(self, sig):
        try:
            super().kill(sig)
        except PermissionError:
            pass

    def wait_timeout(self, timeout):
        try:
            status = self.proc.wait(timeout)
        except TimeoutExpired:
            self.kill('')
            return "TIMEOUT"
        if status >= 0:
            self.exitstatus = status
            self.signalstatus = None
        else:
            self.exitstatus = None
            self.signalstatus = -status
        self.terminated = True
        return status


class TestCase:
    def __init__(self, desc, test_content):
        self.desc = desc
        self.test_content = test_content

    def run_test(self, exe_file):
        console = SafeConsole(exe_file, encoding='cp949')
        for io, *content in self.test_content:
            to_match = content[0]
            isnt_inverse = content[-1]
            if io == "IN":
                console.sendline(to_match)
            elif io == "OUT":
                if to_match == "TERMINATION":
                    if console.wait_timeout(2) not in [-1, 0, 1]:
                        console.kill('')
                        return False, "(Didn't terminate successfully)"
                    continue
                elif to_match == "EXCEPTION":
                    if console.wait_timeout(2) in [-1, 0, 1]:
                        console.kill('')
                        return False, "(Didn't raise an exception)"
                    continue

                try:
                    console.expect(to_match, timeout=2)
                    if not isnt_inverse:
                        console.kill('')
                        return False, console.before + (console.after if type(console.after) == str else '')
                except TIMEOUT:
                    if isnt_inverse:
                        console.kill('')
                        return False, console.before + (console.after if type(console.after) == str else '')
                except EOF:
                    result = console.before.replace('\r\n', ' ') + ' '
                    if type(to_match) == list:
                        for to_match_element in to_match:
                            if not findall(to_match_element, result):
                                console.kill('')
                                if isnt_inverse:
                                    return False, console.before + (console.after if type(console.after) == str else '')
                    else:
                        if not findall(to_match, result):
                            console.kill('')
                            if isnt_inverse:
                                return False, console.before + (console.after if type(console.after) == str else '')

            elif io == "INSERT":
                pass
            else:
                raise Exception
        console.kill('')
        return True, None

    @staticmethod
    def get_regex_contains(*args):
        arg_set = set(args)
        pattern = '^'
        for arg in arg_set:
            pattern += r'(?=(?:.*(?<!\d)' + str(arg) + r'(?![\d-])){' + str(args.count(arg)) + '})'
        pattern += '.+$'

        return pattern
