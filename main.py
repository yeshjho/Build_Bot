import discord
from discord import Embed
from discord.channel import DMChannel
import asyncio
from glob import glob
from importlib import import_module
from multiprocessing import Pool
from os import remove
from os.path import dirname, abspath, isfile
from sys import path as sys_path
from pexpect.popen_spawn import PopenSpawn as Console
from pexpect import TIMEOUT
from datetime import datetime, timedelta
import re
from texts import TEXT

VERSION = '1.3.1'
BOT_KEY = "NjIyNDI1MTc3MTAzMjY5ODk5.XX8nNA.imnCrShejzI8m_oqwRA2w6QiCDw"

TOP_FOLDER = dirname(abspath(__file__)).replace('\\', '/') + '/'
CL_COMMAND = '"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Visual Studio 2019/Visual Studio Tools/' \
             'Developer Command Prompt for VS 2019.lnk"'

RED = 0xff0000
BLUE = 0x0000ff

SUPPORTED_EXTENSION = "cpp"
COMMAND_PREFIX = ">>>"
COOL_TIME_IN_MIN = 10

IS_TESTING = True
TESTER_ID = 353886187879923712

# https://discordapp.com/api/oauth2/authorize?client_id=622425177103269899&permissions=8&scope=bot

# TODO: 블랙리스트
# TODO: 테스트 케이스 목록 열람 명령어(열람하기 전에 직접 생각해 보는 게 좋다는 경고)


sys_path.insert(0, './tests/')


class SafeConsole(Console):
    def kill(self, sig):
        try:
            super().kill(sig)
        except PermissionError:
            pass


class TestResult:
    def __init__(self, assignment, test_result, actual_outputs, error_result):
        self.assignment = assignment
        self.test_result = test_result
        self.actual_outputs = actual_outputs
        self.error_result = error_result

    def get_embeds(self, pfea):
        embeds = []
        index = 0
        for has_passed in self.test_result:
            test_case = self.assignment.tests[index]

            embed = Embed()
            embed.title = TEXT.EMBED.TEST_NUM + str(index).zfill(2) + " - " + \
                          (TEXT.EMBED.TEST_PASSED if has_passed else TEXT.EMBED.TEST_FAILED)
            embed.description = test_case.desc
            embed.colour = BLUE if has_passed else RED

            input_text = '```\n'
            output_text = '```\n'
            for io, *content in test_case.test_content:
                if io == TEXT.TESTCASE.INPUT or io == TEXT.TESTCASE.INSERT:
                    input_text += content[0] + '\n'
                elif io == TEXT.TESTCASE.OUTPUT:
                    output_text += content[1] + '\n'
                else:
                    raise Exception
            embed.add_field(name=TEXT.EMBED.INPUT, value=input_text + '```', inline=False)
            embed.add_field(name=TEXT.EMBED.EXPECTED_OUTPUT, value=output_text + '```', inline=False)

            if not has_passed:
                embed.add_field(name=TEXT.EMBED.ACTUAL_OUTPUT, value='```' + self.actual_outputs[index] + '```',
                                inline=False)

            if (TEXT.EMBED.SEE_ALL in pfea) or (TEXT.EMBED.SEE_PASSED in pfea and has_passed) or \
                    (TEXT.EMBED.SEE_FAILED in pfea and not has_passed):
                embeds.append(embed)

            index += 1

        index = 0
        for has_passed in self.error_result:
            if not has_passed:
                test_case = self.assignment.error_tests[index]

                embed = Embed()
                embed.title = TEXT.EMBED.ERROR_NUM + str(index).zfill(2)
                embed.colour = 0xff0000

                embed.add_field(name=test_case.title, value=test_case.desc)

                if (TEXT.EMBED.SEE_ALL in pfea) or (TEXT.EMBED.SEE_ERROR in pfea):
                    embeds.append(embed)

            index += 1

        return embeds


class BuildBot(discord.Client):
    def __init__(self):
        super().__init__()

        self.testing_user = {}
        self.test_result = {}
        self.last_compile_time = {}

    @staticmethod
    async def on_ready():
        print("Build Bot is ready!")

    async def on_message(self, msg):
        if msg.author == self.user:
            return

        if type(msg.channel) != DMChannel:
            return

        if msg.attachments:
            if IS_TESTING and msg.author.id != TESTER_ID:
                await msg.channel.send(TEXT.OTHER.TESTING)
                return

            if not await self.passed_cool_time(msg):
                return

            attachment = msg.attachments[0]
            cpp_path = await self.save_file(msg, attachment)
            if cpp_path:
                test_result = None

                log("Saved a cpp file of", msg.author.name, "as", cpp_path.split('/')[-1])
                assignment = await self.query_assignment(msg, cpp_path)
                if assignment.is_unittest:
                    exe_paths = await self.compile_files(msg, cpp_path, assignment)
                    if exe_paths:
                        log("Compiled files of", msg.author.name, "as", [path.split('/')[-1] for path in exe_paths])
                        test_result = await self.test_file(msg, cpp_path, exe_paths, assignment)
                else:
                    exe_path = await self.compile_file(msg, cpp_path)
                    if exe_path:
                        log("Compiled a file of", msg.author.name, "as", exe_path.split('/')[-1])
                        test_result = await self.test_file(msg, cpp_path,
                                                           [exe_path] * len(assignment.tests), assignment)

                if test_result:
                    log("Test Result of", msg.author.name, "on", test_result.assignment.__name__, ": ",
                        test_result.test_result, ',', test_result.error_result)
                    self.test_result[msg.author.id] = test_result

        elif msg.author.id in self.test_result and len(msg.content) == 1 and msg.content.upper() in 'PFEA':
            for embed in self.test_result[msg.author.id].get_embeds(msg.content.upper()):
                await msg.channel.send(embed=embed)

        elif msg.content.startswith(COMMAND_PREFIX):
            log(msg.author.name, "Tried to use command", msg.content)
            await self.run_command(msg)

    async def save_file(self, msg, attachment):
        if attachment.filename.split('.')[-1] != SUPPORTED_EXTENSION:
            await msg.channel.send(TEXT.SAVE.SUPPORTED_FILE_EXTENSION)
            return

        self.testing_user[attachment.id] = msg.author.id
        cpp_path = TOP_FOLDER + 'received/' + str(attachment.id) + '.' + SUPPORTED_EXTENSION
        with open(cpp_path, 'wb') as file:
            await attachment.save(file, use_cached=False)
        await msg.channel.send(TEXT.SAVE.RECEIVED)

        return cpp_path

    async def passed_cool_time(self, msg):
        if msg.author.id in self.last_compile_time:
            delta = datetime.now() - self.last_compile_time[msg.author.id]
            if delta < timedelta(minutes=COOL_TIME_IN_MIN):
                delta = timedelta(minutes=COOL_TIME_IN_MIN) - delta
                await msg.channel.send(TEXT.SAVE.COOL_TIME_1 + str(delta.seconds // 60) + TEXT.SAVE.COOL_TIME_2 +
                                       str(delta.seconds % 60) + TEXT.SAVE.COOL_TIME_3)
                return False
        return True

    async def query_assignment(self, msg, cpp_path):
        await msg.channel.send(TEXT.SAVE.QUERY_ASSIGNMENT)
        assignments = [x.split('\\')[-1].split('.')[0] for x in glob("tests/*.py")]
        await msg.channel.send('\n'.join([convert_number_to_emoji(x) + " " + y for x, y in enumerate(assignments)]))

        file_id = int(cpp_path.split('/')[-1].split('.')[0])
        while True:
            response = await self.wait_for("message", check=lambda m: m.author.id == self.testing_user[file_id])
            response = response.content
            if response.isdigit() and 0 <= int(response) <= len(assignments) - 1:
                break
            await msg.channel.send(TEXT.SAVE.TRY_AGAIN)

        return import_module(assignments[int(response)])

    async def compile_file(self, msg, cpp_path, is_unittest=False):
        if not is_unittest:
            await msg.channel.send(TEXT.COMPILE.COMPILING)
            self.last_compile_time[msg.author.id] = datetime.now()

        console = SafeConsole('cmd', encoding='cp949')
        console.sendline(CL_COMMAND)

        obj_path = cpp_path + ".obj"
        exe_path = cpp_path + ".exe"
        console.sendline("cl /Fe" + exe_path + ' /Fo' + obj_path + " " + cpp_path +
                         " /I" + TOP_FOLDER + "/external_libraries" + " /EHsc")

        try:
            expect_index = console.expect_exact(['error', 'out'])
            if expect_index:
                if not is_unittest:
                    await msg.channel.send(TEXT.COMPILE.SUCCESS)
                console.kill('')
                return exe_path
            else:
                console.expect_exact('C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community>')
                detail = console.before
                # remove(cpp_path)
                if not is_unittest:
                    await msg.channel.send(embed=Embed(title=TEXT.COMPILE.FAIL, color=0xff0000))
                    await msg.channel.send(detail[:2000])
                console.kill('')
        except TIMEOUT:
            # remove(cpp_path)
            if not is_unittest:
                await msg.channel.send(embed=Embed(title=TEXT.COMPILE.FAIL, color=0xff0000))
                await msg.channel.send(TEXT.COMPILE.TIMEOUT)
            console.kill('')

        if isfile(cpp_path + ".obj"):
            remove(cpp_path + ".obj")

    async def compile_files(self, msg, cpp_path, assignment):
        await msg.channel.send(TEXT.COMPILE.COMPILING)
        self.last_compile_time[msg.author.id] = datetime.now()

        with open(cpp_path, encoding='utf-8') as original_file:
            original_code = original_file.read()

        re.sub(r'/\*([\s\S]*?)\*/|//.*\n', '', original_code)

        unittest_paths = []
        index = 0
        for test_case in assignment.tests:
            index += 1
            for io, *content in test_case.test_content:
                if io == TEXT.TESTCASE.INSERT:
                    unittest_code = re.sub(r'int\s+main\s*\(.*\)\s*{', 'int main() {\n' + content[0] + "\nreturn 0;",
                                           original_code)
                    unittest_path = cpp_path[:-4] + "_unittest_" + str(index) + '.' + SUPPORTED_EXTENSION
                    with open(unittest_path, "a+", encoding='utf-8') as unittest_file:
                        unittest_file.write(unittest_code)
                    unittest_paths.append(unittest_path)

        length = len(assignment.tests)
        with Pool(length) as pool:
            exe_paths = pool.map(compile_file, unittest_paths)
            if all(exe_paths):
                await msg.channel.send(TEXT.COMPILE.SUCCESS)

                return exe_paths
            else:
                await msg.channel.send(embed=Embed(title=TEXT.COMPILE.FAIL, color=0xff0000))

    async def test_file(self, msg, cpp_path, exe_paths, assignment):
        await msg.channel.send(TEXT.TEST.TESTING)

        test_outcome = None
        try:
            with Pool(len(assignment.tests)) as pool:
                test_outcome = pool.starmap(run_test, zip(assignment.tests, exe_paths))
        except ...:
            self.last_compile_time[msg.author.id] = datetime(2000, 1, 1)
            await msg.channel.send(TEXT.TEST.FAIL)
            return

        test_result = [outcome[0] for outcome in test_outcome]
        actual_outputs = [outcome[1] for outcome in test_outcome]
        error_result = [test.run_test(cpp_path) for test in assignment.error_tests]

        await msg.channel.send(TEXT.TEST.COMPLETE)

        pass_count = test_result.count(True)
        fail_count = test_result.count(False)
        error_count = error_result.count(False)
        percentage = round(pass_count / len(test_result) * 100)

        embed = Embed()
        embed.title = TEXT.EMBED.TEST_RESULT + str(percentage) + "%" + \
                      (TEXT.EMBED.TEST_RESULT_WITH_ERROR if error_count else '')
        embed.colour = round((100 - percentage) / 100 * 255) * 16 ** 4 + round(percentage / 100 * 255)
        embed.add_field(name=TEXT.EMBED.PASSED_COUNT + str(pass_count), value='\u200b')
        embed.add_field(name=TEXT.EMBED.FAILED_COUNT + str(fail_count), value='\u200b')
        embed.add_field(name=TEXT.EMBED.ERROR_COUNT + str(error_count), value='\u200b')
        await msg.channel.send(embed=embed)

        to_send = ""
        if pass_count:
            to_send += TEXT.TEST.SEE_PASSED
        if fail_count:
            to_send += TEXT.TEST.SEE_FAILED
        if error_count:
            to_send += TEXT.TEST.SEE_ERROR
        await msg.channel.send(to_send + TEXT.TEST.SEE_ALL)

        # remove(exe_path[:-4])
        for exe_path in exe_paths:
            if isfile(exe_path[:-4] + ".obj"):
                remove(exe_path[:-4] + ".obj")
        # remove(exe_path)

        return TestResult(assignment, test_result, actual_outputs, error_result)

    async def run_command(self, msg):
        commands = msg.content.split(' ')
        command = commands[0][3:]

        if command == TEXT.COMMAND.COOLTIME:
            if len(commands) == 1:
                self.last_compile_time[msg.author.id] = datetime(2000, 1, 1)
            else:
                self.last_compile_time[int(commands[1])] = datetime(2000, 1, 1)
        elif command == TEXT.COMMAND.VERSION:
            await msg.channel.send(VERSION)


def compile_file(cpp_path):
    console = SafeConsole('cmd', encoding='cp949')
    console.sendline(CL_COMMAND)

    obj_path = cpp_path + ".obj"
    exe_path = cpp_path + ".exe"
    console.sendline("cl /Fe" + exe_path + ' /Fo' + obj_path + " " + cpp_path +
                     " /I" + TOP_FOLDER + "/external_libraries" + " /EHsc")

    try:
        expect_index = console.expect_exact(['error', 'out'])
        console.kill('')
        if expect_index:
            return exe_path
        else:
            # remove(cpp_path)
            pass
    except TIMEOUT:
        # remove(cpp_path)
        console.kill('')


def run_test(instance, file_path):
    return instance.run_test(file_path)


def convert_number_to_emoji(num):
    if num == 10:
        return ":keycap_ten:"
    elif num == 0:
        return ":zero:"

    numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    to_return = ""
    while num:
        cipher = num % 10
        num //= 10
        to_return = ":" + numbers[cipher] + ":" + to_return

    return to_return


def log(*texts):
    path = TOP_FOLDER + '/logs/' + str(datetime.now().date()) + ".txt"
    with open(path, 'a+', encoding='utf-8') as log_file:
        log_file.write("[" + str(datetime.now().time())[:-7] + "]: " + " ".join(map(str, texts)) + "\n")


if __name__ == "__main__":
    build_bot = BuildBot()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(build_bot.start(BOT_KEY))
    except KeyboardInterrupt:
        loop.run_until_complete(build_bot.logout())
    finally:
        loop.close()
