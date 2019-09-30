from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase("Two Roots - a≠0, b≠0, c≠0", [
        ("INSERT", "SolveQuadEquation(1.0, -3.0, 2.0);"),
        ("OUT", TestCase.get_regex_contains("root [12] : 1", "root [12] : 2"), "root 1 : 1\nroot 2 : 2")
    ]),
    TestCase("One Root - a≠0, b≠0, c≠0", [
        ("INSERT", "SolveQuadEquation(1.0, -2.0, 1.0);"),
        ("OUT", r"\broot : 1\b", "root : 1")
    ]),
    TestCase("No Root - a≠0, b≠0, c≠0", [
        ("INSERT", "SolveQuadEquation(1.0, 1.0, 1.0);"),
        ("OUT", TestCase.get_regex_contains("root : "), 'NOT "root : "', False),
        ("OUT", "EXCEPTION", "(An exception should be thrown)")
    ]),
    TestCase("Two Roots - a≠0, b≠0, c=0", [
        ("INSERT", "SolveQuadEquation(1.0, 1.0, 0.0);"),
        ("OUT", TestCase.get_regex_contains("root [12] : 0", "root [12] : -1"), "root 1 : 0\nroot 2 : -1")
    ]),
    TestCase("Two Roots - a≠0, b=0, c≠0", [
        ("INSERT", "SolveQuadEquation(4.0, 0.0, -1.0);"),
        ("OUT", TestCase.get_regex_contains("root [12] : 0.5", "root [12] : -0.5"), "root 1 : 0.5\nroot 2 : -0.5")
    ]),
    TestCase("No Root - a≠0, b=0, c≠0", [
        ("INSERT", "SolveQuadEquation(1.0, 0.0, 1.0);"),
        ("OUT", TestCase.get_regex_contains("root : "), 'NOT "root : "', False),
        ("OUT", "EXCEPTION", "(An exception should be thrown)")
    ]),
    TestCase("One Root - a=0, b≠0, c≠0", [
        ("INSERT", "SolveQuadEquation(0.0, 2.0, 1.0);"),
        ("OUT", r"\b-0.5\b", "-0.5")
    ]),
    TestCase("One Root - a≠0, b=0, c=0", [
        ("INSERT", "SolveQuadEquation(5.0, 0.0, 0.0);"),
        ("OUT", r"\broot : (-)?0\b", "root : 0")
    ]),
    TestCase("One Root - a=0, b≠0, c=0", [
        ("INSERT", "SolveQuadEquation(0.0, 5.0, 0.0);"),
        ("OUT", r"\b(-)?0\b", "0")
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
