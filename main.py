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

TOP_FOLDER = dirname(abspath(__file__)).replace('\\', '/') + '/'
CL_COMMAND = '"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Visual Studio 2019/Visual Studio Tools/' \
             'Developer Command Prompt for VS 2019.lnk"'
COOL_TIME_IN_MIN = 10
VERSION = '1.2.1'

sys_path.insert(0, './tests/')

# https://discordapp.com/api/oauth2/authorize?client_id=622425177103269899&permissions=8&scope=bot

# TODO: 실제 아웃풋 알려주기
# TODO: 테스트 케이스 파일에 is_unittest 해놓고 그거로 유닛테스트인지 아닌지 체크
# TODO: 텍스트들 다 분리하기
# TODO: 블랙리스트
# TODO: 테스트 케이스 목록 열람 명령어(열람하기 전에 직접 생각해 보는 게 좋다는 경고)


class SafeConsole(Console):
    def kill(self, sig):
        try:
            super().kill(sig)
        except PermissionError:
            pass


class TestResult:
    def __init__(self, assignment, test_result, error_result):
        self.assignment = assignment
        self.test_result = test_result
        self.error_result = error_result

    def get_embeds(self, pfea):
        embeds = []
        index = 0
        for has_passed in self.test_result:
            test_case = self.assignment.tests[index]

            embed = Embed()
            embed.title = 'Test #' + str(index).zfill(2) + " - " + ("Passed" if has_passed else "Failed")
            embed.description = test_case.desc
            embed.colour = 0x0000ff if has_passed else 0xff0000

            input_text = '```\n'
            output_text = '```\n'
            for io, *content in test_case.test_content:
                if io == "IN" or io == "INSERT":
                    input_text += content[0] + '\n'
                elif io == "OUT":
                    output_text += content[1] + '\n'
                else:
                    raise Exception
            embed.add_field(name="Input", value=input_text + '```', inline=False)
            embed.add_field(name="Expected Output", value=output_text + '```', inline=False)

            if ('A' in pfea) or ('P' in pfea and has_passed) or ('F' in pfea and not has_passed):
                embeds.append(embed)

            index += 1

        index = 0
        for has_passed in self.error_result:
            if not has_passed:
                test_case = self.assignment.error_tests[index]

                embed = Embed()
                embed.title = 'Error #' + str(index).zfill(2)
                embed.colour = 0xff0000

                embed.add_field(name=test_case.title, value=test_case.desc)

                if ('A' in pfea) or ('E' in pfea):
                    embeds.append(embed)

            index += 1

        return embeds


class BuildBot(discord.Client):
    def __init__(self):
        super().__init__()

        self.unittests = ['cs120_chapter_5_exercise_task1']
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

        elif msg.content.startswith('>>>'):
            log(msg.author.name, "Tried to use command", msg.content)
            await self.run_command(msg)

    async def save_file(self, msg, attachment):
        if attachment.filename.split('.')[-1] != 'cpp':
            await msg.channel.send("Only cpp files are supported")
            return

        self.testing_user[attachment.id] = msg.author.id
        cpp_path = TOP_FOLDER + 'received/' + str(attachment.id) + '.cpp'
        with open(cpp_path, 'wb') as file:
            await attachment.save(file, use_cached=False)
        await msg.channel.send("File received")

        return cpp_path

    async def passed_cool_time(self, msg):
        if msg.author.id in self.last_compile_time:
            delta = datetime.now() - self.last_compile_time[msg.author.id]
            if delta < timedelta(minutes=COOL_TIME_IN_MIN):
                delta = timedelta(minutes=COOL_TIME_IN_MIN) - delta
                await msg.channel.send("Whoa, too fast!\nYou have to wait for `" +
                                       str(delta.seconds // 60) + " minutes and " +
                                       str(delta.seconds % 60) + " seconds` for another attempt")
                return False
        return True
        
    async def query_assignment(self, msg, cpp_path):
        await msg.channel.send("What assignment is this for? Please enter a number")
        assignments = [x.split('\\')[-1].split('.')[0] for x in glob("tests/*.py")]
        await msg.channel.send('\n'.join([convert_number_to_emoji(x) + " " + y for x, y in enumerate(assignments)]))

        file_id = int(cpp_path.split('/')[-1].split('.')[0])
        while True:
            response = await self.wait_for("message", check=lambda m: m.author.id == self.testing_user[file_id])
            response = response.content
            if response.isdigit() and 0 <= int(response) <= len(assignments) - 1:
                break
            await msg.channel.send("Please try again")
            
        return import_module(assignments[int(response)])

    async def compile_file(self, msg, cpp_path, is_unittest=False):
        if not is_unittest:
            await msg.channel.send("Compiling...")
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
                    await msg.channel.send("Compilation Succeeded")
                console.kill('')
                return exe_path
            else:
                console.expect_exact('C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community>')
                detail = console.before
                # remove(cpp_path)
                if not is_unittest:
                    await msg.channel.send(embed=Embed(title=":no_entry: Compilation Failed", color=0xff0000))
                    await msg.channel.send(detail[:2000])
                console.kill('')
        except TIMEOUT:
            # remove(cpp_path)
            if not is_unittest:
                await msg.channel.send(embed=Embed(title=":no_entry: Compilation Failed", color=0xff0000))
                await msg.channel.send("Timed out")
            console.kill('')
        
        if isfile(cpp_path + ".obj"):
            remove(cpp_path + ".obj")

    async def compile_files(self, msg, cpp_path, assignment):
        await msg.channel.send("Compiling...")
        self.last_compile_time[msg.author.id] = datetime.now()

        with open(cpp_path, encoding='utf-8') as original_file:
            original_code = original_file.read()

        re.sub(r'/\*([\s\S]*?)\*/|//.*\n', '', original_code)

        unittest_paths = []
        index = 0
        for test_case in assignment.tests:
            index += 1
            for io, *content in test_case.test_content:
                if io == "INSERT":
                    unittest_code = re.sub(r'int\s+main\s*\(.*\)\s*{', 'int main() {\n' + content[0] + "\nreturn 0;",
                                           original_code)
                    unittest_path = cpp_path[:-4] + "_unittest_" + str(index) + ".cpp"
                    with open(unittest_path, "a+", encoding='utf-8') as unittest_file:
                        unittest_file.write(unittest_code)
                    unittest_paths.append(unittest_path)

        length = len(assignment.tests)
        with Pool(length) as pool:
            exe_paths = pool.map(compile_file, unittest_paths)
            if all(exe_paths):
                await msg.channel.send("Compilation Succeeded")
                
                return exe_paths
            else:
                await msg.channel.send(embed=Embed(title=":no_entry: Compilation Failed", color=0xff0000))

    @staticmethod
    async def test_file(msg, cpp_path, exe_paths, assignment):
        await msg.channel.send("Testing...")
        with Pool(len(assignment.tests)) as pool:
            test_result = pool.starmap(run_test, zip(assignment.tests, exe_paths))
        error_result = [test.run_test(cpp_path) for test in assignment.error_tests]
        await msg.channel.send("Test complete")

        pass_count = test_result.count(True)
        fail_count = test_result.count(False)
        error_count = error_result.count(False)
        percentage = round(pass_count / len(test_result) * 100)

        embed = Embed()
        embed.title = 'Test Result: ' + str(percentage) + "%" + (" with errors" if error_count else '')
        embed.colour = round((100 - percentage) / 100 * 255) * 16 ** 4 + round(percentage / 100 * 255)
        embed.add_field(name="Passed Tests: " + str(pass_count), value='\u200b')
        embed.add_field(name="Failed Tests: " + str(fail_count), value='\u200b')
        embed.add_field(name="Other Errors: " + str(error_count), value='\u200b')
        await msg.channel.send(embed=embed)

        to_send = ""
        if pass_count:
            to_send += "Type **`P`** to examine what tests you've passed\n"
        if fail_count:
            to_send += "Type **`F`** to examine what tests you've failed\n"
        if error_count:
            to_send += "Type **`E`** to examine what errors you've got\n"
        await msg.channel.send(to_send + "Type **`A`** to examine all")

        # remove(exe_path[:-4])
        for exe_path in exe_paths:
            if isfile(exe_path[:-4] + ".obj"):
                remove(exe_path[:-4] + ".obj")
        # remove(exe_path)

        return TestResult(assignment, test_result, error_result)

    async def run_command(self, msg):
        commands = msg.content.split(' ')
        command = commands[0][3:]

        if command == 'cooltime':
            if len(commands) == 1:
                self.last_compile_time[msg.author.id] = datetime(2000, 1, 1)
            else:
                self.last_compile_time[int(commands[1])] = datetime(2000, 1, 1)
        elif command == 'version':
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
        loop.run_until_complete(build_bot.start("NjIyNDI1MTc3MTAzMjY5ODk5.XX8nNA.imnCrShejzI8m_oqwRA2w6QiCDw"))
    except KeyboardInterrupt:
        loop.run_until_complete(build_bot.logout())
    finally:
        loop.close()
