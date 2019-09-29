from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase("Valid 1", [
        ("IN", "2"),
        ("OUT", r"\b1\b", "1")
    ]),
    TestCase("Valid 2", [
        ("IN", "7"),
        ("OUT", r"\b13\b", "13")
    ]),
    TestCase("OUT OF RANGE 1", [
        ("IN", "0"),
        ("OUT", [TestCase.get_regex_contains(-1), TestCase.get_regex_contains(0),
                 TestCase.get_regex_contains(1), TestCase.get_regex_contains(2)], "NOT -1 or 0 or 1 or 2", False),
        ("OUT", "TERMINATION", "(Some words and normal termination)"
                               "(I can only detect exit code -1, 0, and 1, "
                               "other exit codes are OK if it's provided by you)")
    ]),
    TestCase("OUT OF RANGE 2", [
        ("IN", "-10"),
        ("OUT", [TestCase.get_regex_contains(-1), TestCase.get_regex_contains(0),
                 TestCase.get_regex_contains(1), TestCase.get_regex_contains(2)], "NOT -1 or 0 or 1 or 2", False),
        ("OUT", "TERMINATION", "(Some words and normal termination)"
                               "(I can only detect exit code -1, 0, and 1, "
                               "other exit codes are OK if it's provided by you)")
    ]),
    TestCase("OUT OF RANGE 3", [
        ("IN", "46"),
        ("OUT", r"\b1836311903\b", "NOT 1836311903", False),
        ("OUT", "TERMINATION", "(Some words and normal termination)"
                               "(I can only detect exit code -1, 0, and 1, "
                               "other exit codes are OK if it's provided by you)")
    ]),
    TestCase("Invalid", [
        ("IN", "a"),
        ("OUT", [TestCase.get_regex_contains(-1), TestCase.get_regex_contains(0),
                 TestCase.get_regex_contains(1), TestCase.get_regex_contains(2)], "NOT -1 or 0 or 1 or 2", False),
        ("OUT", "TERMINATION", "(Some words and normal termination)"
                               "(I can only detect exit code -1, 0, and 1, "
                               "other exit codes are OK if it's provided by you)")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120'))
]
