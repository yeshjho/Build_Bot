from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase("Two Roots - a≠0, b≠0, c≠0", [
        ("INSERT", "SolveQuadEquation(1.0, -3.0, 2.0);"),
        ("OUT", TestCase.get_regex_contains("1", "2"), "(Contains 1 and 2 regardless of order)")
    ]),
    TestCase("One Root - a≠0, b≠0, c≠0", [
        ("INSERT", "SolveQuadEquation(1.0, -2.0, 1.0);"),
        ("OUT", TestCase.get_regex_contains("1"), "1")
    ]),
    TestCase("No Root - a≠0, b≠0, c≠0", [
        ("INSERT", "SolveQuadEquation(1.0, 1.0, 1.0);"),
        ("OUT", TestCase.get_regex_contains("root : "), 'NOT "root : "', False),
        ("OUT", "EXCEPTION", "(An exception should be thrown)")
    ]),
    TestCase("Two Roots - a≠0, b≠0, c=0", [
        ("INSERT", "SolveQuadEquation(1.0, 1.0, 0.0);"),
        ("OUT", TestCase.get_regex_contains("0", "-1"), "(Contains 0 and -1 regardless of order)")
    ]),
    TestCase("Two Roots - a≠0, b=0, c≠0", [
        ("INSERT", "SolveQuadEquation(4.0, 0.0, -1.0);"),
        ("OUT", TestCase.get_regex_contains("0.5", "-0.5"), "(Contains 0.5 and -0.5 regardless of order)")
    ]),
    TestCase("No Root - a≠0, b=0, c≠0", [
        ("INSERT", "SolveQuadEquation(1.0, 0.0, 1.0);"),
        ("OUT", TestCase.get_regex_contains("root : "), 'NOT "root : "', False),
        ("OUT", "EXCEPTION", "(An exception should be thrown)")
    ]),
    TestCase("One Root - a=0, b≠0, c≠0", [
        ("INSERT", "SolveQuadEquation(0.0, 2.0, 1.0);"),
        ("OUT", TestCase.get_regex_contains("-0.5"), "-0.5")
    ]),
    TestCase("One Root - a≠0, b=0, c=0", [
        ("INSERT", "SolveQuadEquation(5.0, 0.0, 0.0);"),
        ("OUT", TestCase.get_regex_contains(r"(-)?0"), "0")
    ]),
    TestCase("One Root - a=0, b≠0, c=0", [
        ("INSERT", "SolveQuadEquation(0.0, 5.0, 0.0);"),
        ("OUT", TestCase.get_regex_contains(r"(-)?0"), "0")
    ]),
    TestCase("No Root - a=0, b=0, c≠0", [
        ("INSERT", "SolveQuadEquation(0.0, 0.0, 5.0);"),
        ("OUT", TestCase.get_regex_contains("root : "), 'NOT "root : "', False),
        ("OUT", "EXCEPTION", "(An exception should be thrown)")
    ]),
    TestCase("Identity - a=0, b=0, c=0", [
        ("INSERT", "SolveQuadEquation(0.0, 0.0, 0.0);"),
        ("OUT", TestCase.get_regex_contains("root : "), 'NOT "root : "', False)
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120'))
]
