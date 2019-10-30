from test_case import TestCase
from error_test import ErrorTest

is_unittest = False

tests = [
    TestCase("Logic Error 1", [
        ("IN", "(1+2)*3;"),
        ("OUT", TestCase.get_regex_contains('= 9'), '= 9')
    ]),
    TestCase("Logic Error 2", [
        ("IN", "+1*3;"),
        ("OUT", TestCase.get_regex_contains('= 3'), '= 3')
    ]),
    TestCase("Logic Error 3", [
        ("IN", "(1;"),
        ("OUT", TestCase.get_regex_contains(r"'\)' expected"), "')' expected")
    ]),
    TestCase("Logic Error 4", [
        ("IN", "let a = 4;"),
        ("OUT", TestCase.get_regex_contains('= 4'), '= 4')
    ]),
    TestCase("Logic Error 5", [
        ("IN", "let a = 3;"),
        ("OUT", TestCase.get_regex_contains('= 3'), '= 3'),
        ("IN", "let b = 2;"),
        ("OUT", TestCase.get_regex_contains('= 2'), '= 2')
    ]),
    TestCase("Logic Error 6", [
        ("IN", "9%2;"),
        ("OUT", TestCase.get_regex_contains('= 1'), '= 1')
    ]),
    TestCase("Logic Error 7", [
        ("IN", "12%5*2+3;"),
        ("OUT", TestCase.get_regex_contains('= 7'), '= 7')
    ]),
    TestCase("Logic Error 8", [
        ("IN", "9%0"),
        ("OUT", TestCase.get_regex_contains(r'(0|zero)'), '(error message contains "0" or "zero")')
    ]),
    TestCase("Logic Error 9", [
        ("IN", "q;"),
        ("OUT", "TERMINATION", "Normal termination")
    ]),
    TestCase("Logic Error 10", [
        ("IN", "q"),
        ("OUT", r"Please enter .+ to exit", "(keeping window open)")
    ]),
    TestCase("Logic Error 11", [
        ("IN", "4+2-5+8;"),
        ("OUT", TestCase.get_regex_contains('= 9'), '= 9')
    ]),
    TestCase("Check Working - Variables", [
        ("IN", "let a = 3;"),
        ("OUT", TestCase.get_regex_contains('= 3'), '= 3'),
        ("IN", "let b = 2;"),
        ("OUT", TestCase.get_regex_contains('= 2'), '= 2'),
        ("IN", "let c = a*2+b;"),
        ("OUT", TestCase.get_regex_contains('= 8'), '= 8'),
        ("IN", "c%3;"),
        ("OUT", TestCase.get_regex_contains('= 2'), '= 2')
    ]),
    TestCase("Check Not Working - Redeclaring a Variable", [
        ("IN", "let b = 1;"),
        ("OUT", TestCase.get_regex_contains('= 1'), '= 1'),
        ("IN", "let b = 3;"),
        ("OUT", TestCase.get_regex_contains('= 3'), "NOT = 3", False)
    ]),
    TestCase("Check Working - Calculating", [
        ("IN", "12*(3-1)%13*3+-4+6/3/1*2;"),
        ("OUT", TestCase.get_regex_contains('= 33'), '= 33')
    ]),
    TestCase("Check Working - Quitting", [
        ("IN", "quit"),
        ("OUT", "TERMINATION", "Normal termination")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120')),
    ErrorTest("Hard Coding 1", "Your code contains hard coding",
              ErrorTest.get_function_contains("t.kind != 'a'", should_contain=False)),
    ErrorTest("Hard Coding 2", "Your code contains hard coding",
              ErrorTest.get_function_contains("case ';':", should_contain=False))
]
