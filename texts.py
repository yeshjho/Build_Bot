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
        SUPPORTED_FILE_EXTENSION = "Only cpp files are supported"
        RECEIVED = "File received"

        COOL_TIME_1 = "Whoa, too fast!\nYou have to wait for `"
        COOL_TIME_2 = " minutes and "
        COOL_TIME_3 = " seconds` for another attempt"

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

        SEE_PASSED = "Type :regional_indicator_p: to examine what tests you've passed\n"
        SEE_FAILED = "Type :regional_indicator_f: to examine what tests you've failed\n"
        SEE_ERROR = "Type :regional_indicator_e: to examine what errors you've got\n"
        SEE_ALL = "Type :regional_indicator_a: to examine all"

    class OTHER:
        TESTING = "Sorry! Currently Testing!"

    class COMMAND:
        COOLTIME = "cooltime"
        VERSION = "version"
