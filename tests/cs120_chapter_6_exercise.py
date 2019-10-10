from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase("Normal Input", [
        ("IN", "10 2"),
        ("IN", "b"),
        ("OUT", TestCase.get_regex_contains(r"P\(10,2\) = 90", r"C\(10,2\) = 45"), "P(10,2) = 90\nC(10,2) = 45")
    ]),
    TestCase("Abnormal Input - Not Numbers", [
        ("IN", "ab 20"),
        ("IN", "b"),
        ("OUT", TestCase.get_regex_contains("="), "NOT =", False)
    ]),
    TestCase("Abnormal Input - n < r", [
        ("IN", "10 20"),
        ("IN", "b"),
        ("OUT", TestCase.get_regex_contains("="), "NOT =", False)
    ]),
    TestCase("Abnormal Input - Negative Number", [
        ("IN", "-20 8"),
        ("IN", "b"),
        ("OUT", TestCase.get_regex_contains("="), "NOT =", False)
    ]),
    TestCase("Abnormal Input - Not p nor c nor b", [
        ("IN", "10 2"),
        ("IN", "q"),
        ("OUT", TestCase.get_regex_contains("="), "NOT =", False)
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120'))
]
