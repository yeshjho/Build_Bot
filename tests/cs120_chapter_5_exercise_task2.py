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
        ("OUT", "TERMINATION", "(Some words and normal termination)")
    ]),
    TestCase("OUT OF RANGE 2", [
        ("IN", "-10"),
        ("OUT", "TERMINATION", "(Some words and normal termination)")
    ]),
    TestCase("OUT OF RANGE 3", [
        ("IN", "46"),
        ("OUT", "1836311903", "NOT 1836311903", True)
    ]),
    TestCase("Invalid", [
        ("IN", "a"),
        ("OUT", "TERMINATION", "(Some words and normal termination)")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120'))
]
