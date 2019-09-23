from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase('Space - Normal', [
        ("IN", "1 2 3 -1 quit 8"),
        ("OUT", TestCase.get_regex_contains(-1, 3, 4, 5), "(Contains -1, 3, 4, and 5 regardless of order)")
    ]),
    TestCase('Space - Character with no whitespace', [
        ("IN", "3 0 5.3 -2"),
        ("OUT", TestCase.get_regex_contains(0, 3, 5, 8), "(Contains 0, 3, 5, and 8 regardless of order)")
    ]),
    TestCase('Space - One Input', [
        ("IN", "-2 quit"),
        ("OUT", TestCase.get_regex_contains(-2, -2, -2, 1), "(Contains -2, -2, -2, and 1 regardless of order)")
    ]),
    TestCase("\\n - Normal", [
        ("IN", "-1\n-2\n-3\n-1\nquit\n8"),
        ("OUT", TestCase.get_regex_contains(-7, -3, -1, 4), "(Contains -7, -3, -1, and 4 regardless of order)")
    ]),
    TestCase("\\n - Character with no whitespace", [
        ("IN", "-5\n3\n0\n5a3\n-2"),
        ("OUT", TestCase.get_regex_contains(-5, 3, 4, 5), "(Contains -5, 3, 4, and 5 regardless of order)")
    ]),
    TestCase("\\n - One Input", [
        ("IN", "4\n."),
        ("OUT", TestCase.get_regex_contains(1, 4, 4, 4), "(Contains 1, 4, 4, and 4 regardless of order)")
    ]),
    TestCase("Mixed - Normal", [
        ("IN", "-3 2\n-3 2\na 9"),
        ("OUT", TestCase.get_regex_contains(-3, -2, 2, 4), "(Contains -3, -2, 2, and 4 regardless of order)")
    ]),
    TestCase("Mixed - Character with no whitespace", [
        ("IN", "-9\n3 0\n5.3 -2"),
        ("OUT", TestCase.get_regex_contains(-9, -1, 4, 5), "(Contains -9, -1, 4, and 5 regardless of order)")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120'))
]
