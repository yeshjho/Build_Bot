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
        for io, *content, is_inverse in self.test_content:
            content = content[0]
            if io == "IN":
                console.sendline(content)
            elif io == "OUT":
                if content == "TERMINATION":
                    if console.wait_timeout(2) not in [-1, 0, 1]:
                        console.kill('')
                        return False
                    continue

                try:
                    console.expect(content, timeout=2)
                    if is_inverse:
                        console.kill('')
                        return False
                except TIMEOUT:
                    if not is_inverse:
                        console.kill('')
                        return False
                except EOF:
                    result = console.before.replace('\r\n', ' ') + ' '
                    if not findall(content, result):
                        console.kill('')
                        if not is_inverse:
                            console.kill('')
                            return False
            else:
                raise Exception
        console.kill('')
        return True

    @staticmethod
    def get_regex_contains(*args):
        arg_set = set(args)
        pattern = '^'
        for arg in arg_set:
            pattern += r'(?=(?:.*(?<!\d)' + str(arg) + r'(?![\d-])){' + str(args.count(arg)) + '})'
        pattern += '.+$'

        return pattern