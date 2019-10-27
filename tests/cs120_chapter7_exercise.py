from test_case import TestCase
from error_test import ErrorTest

is_unittest = False

tests = [
    TestCase("Variable Names with Underscores", [
        ("IN", "let a_b_c = 2;"),
        ("OUT", TestCase.get_regex_contains('= 2'), '= 2')
    ]),
    TestCase("Assigning to a Variable", [
        ("IN", "let a_b_c = 2;"),
        ("OUT", TestCase.get_regex_contains('= 2'), '= 2'),
        ("IN", "a_b_c = 5;"),
        ("OUT", TestCase.get_regex_contains('= 5'), '= 5')
    ]),
    TestCase("Constants", [
        ("IN", "const pi = 3.14;"),
        ("OUT", TestCase.get_regex_contains('= 3.14'), '= 3.14')
    ]),
    TestCase("Assigning to a Constant", [
        ("IN", "const pi = 3.14;"),
        ("OUT", TestCase.get_regex_contains('= 3.14'), '= 3.14'),
        ("IN", "pi = 2;"),
        ("OUT", TestCase.get_regex_contains('= 2'), "NOT = 2", False)
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120')),
]
