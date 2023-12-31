class TEXT:
    class TESTCASE:
        INPUT = "IN"
        OUTPUT = "OUT"
        INSERT = "INSERT"
        TERMINATION = "TERMINATION"
        EXCEPTION = "EXCEPTION"

    class EMBED:
        TEST_RESULT = "Test Result: "
        TEST_RESULT_WITH_ERROR = " with errors"
        PASSED_COUNT = "Passed Tests: "
        FAILED_COUNT = "Failed Tests: "
        ERROR_COUNT = "Other Errors: "

        TEST_NUM = "Test #"
        TEST_PASSED = "Passed"
        TEST_FAILED = "Failed"
        INPUT = "Input"
        EXPECTED_OUTPUT = "Expected Output"
        ACTUAL_OUTPUT = "Actual Output"

        ERROR_NUM = "Error #"

        SEE_PASSED = "P"
        SEE_FAILED = "F"
        SEE_ERROR = "E"
        SEE_ALL = "A"

        ACTUAL_NO_TERMINATION = "(Didn't terminate successfully)"
        ACTUAL_NO_EXCEPTION = "(Didn't raise an exception)"

    class SAVE:
        BLOCKED = "Oops! You're on the blacklist!"

        SUPPORTED_FILE_EXTENSION = "Only cpp files are supported"
        RECEIVED = "File received"

        COOLTIME_WORDS = "Whoa, too fast!\nYou have to wait for `"
        COOLTIME_MINUTE = " minutes and "
        COOLTIME_SECOND = " seconds` for another attempt"

        QUERY_ASSIGNMENT = "What assignment is this for? Please enter a number"
        TRY_AGAIN = "Please try again"

    class COMPILE:
        COMPILING = "Compiling..."
        SUCCESS = "Compilation Succeeded"
        FAIL = ":no_entry: Compilation Failed"
        TIMEOUT = "Timed out"

    class TEST:
        TESTING = "Testing..."
        COMPLETE = "Testing complete"
        FAIL = "Testing failed.\nIt might be my problem, please try again! Resetting your cooltime..."
        
        UNICODE_ERROR = "Error testing failed. Your file must be encoded with UTF-8.\nSkipping error tests..."

        ZERO_WORDS = "You've passed nothing! You may not examine any of the test cases...\nThink for yourself!"

        EMOJIS = {
            0: [":poop:", ":facepalm:", ":shrug:", ":speak_no_evil:", ":weary:", ":scream:", ":sob:", ":dizzy_face:", ":exploding_head:"],
            1: [":tired_face:", ":fearful:", ":flushed:", ":head_bandage:", ":confounded:", ":face_with_hand_over_mouth:"],
            2: [":unamused:", ":worried:", ":cry:", ":cold_sweat:", ":persevere:", ":woozy_face:"],
            3: [":disappointed:", ":frowning2:", ":sweat:", ":pleading_face:"],
            4: [":pensive:", ":confused:", ":slight_frown:", ":disappointed_relieved:"],
            5: [":expressionless:", ":rolling_eyes:", ":face_with_monocle:"],
            6: [":neutral_face:", ":thinking:", ":face_with_raised_eyebrow:"],
            7: [":slight_smile:", ":blush:", ":smirk:", ":cowboy:"],
            8: [":smiley:", ":laughing:", ":wink:", ":relaxed:"],
            9: [":grinning:", ":innocent:", ":hugging:"],
            10: [":yum:", ":sunglasses:", ":heart_eyes:", ":star_struck:", ":partying_face:"]
        }

        SEE_PASSED = "Type :regional_indicator_p: to examine what tests you've passed\n"
        SEE_FAILED = "Type :regional_indicator_f: to examine what tests you've failed\n"
        SEE_ERROR = "Type :regional_indicator_e: to examine what errors you've got\n"
        SEE_ALL = "Type :regional_indicator_a: to examine all"

    class OTHER:
        TESTING = "Sorry! Currently Testing!"
        
        NULL = '\u200b'
        
    class RE:
        COMMENT = r'/\*([\s\S]*?)\*/|//.*\n'
        MAIN = r'int\s+main\s*\(.*\)\s*{'
    
    class CMD:
        START_CL = '"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Visual Studio 2019/Visual Studio Tools/' \
                   'Developer Command Prompt for VS 2019.lnk"'
        COMPILE = "cl /Fe{0} /Fo{1} {2} /I{3}external_libraries /EHsc"
        CL_PROMPT = 'C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community>'

    class PATH:
        SUPPORTED_EXTENSION = "cpp"
        
        TESTCASE_FOLDER = "./tests/"
        RECEIVED_FOLDER = "{0}received/"
        
        PERMISSION_FILE = "permissions.pickle"

    class COMMAND:
        PREFIX = ">>>"
        
        COMMAND_HELP = "help"
        COMMAND_COOLTIME = "cooltime"
        COMMAND_VERSION = "version"
        COMMAND_PERMISSION = "permission"
        COMMAND_ATTRIBUTE = "attribute"
        COMMAND_RELOAD = "reload"

        PERMISSION_COMMAND_SEE_ALL = "ALL"
        PERMISSION_OTHER = "OTHER"

        SUCCESS = "Successfully executed the command"
        NO_PERMISSION = "You're not allowed to use this command!"
        INVALID_ARGUMENT = "Arguments are invalid"
        UNKNOWN_COMMAND = "Unknown command\nType `>>>help` to see all available commands"

    class ATTRIBUTES:
        COOLTIME = "COOLTIME"
