from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase("Logic Error 1", [
        ("IN", "1-5;"),
        ("OUT", "=-4", "=-4")
    ]),
    TestCase("Logic Error 2", [
        ("IN", "2+8;"),
        ("OUT", "=10", "=10")
    ]),
    TestCase("Logic Error 3", [
        ("IN", "1+2*5;"),
        ("OUT", "=11", "=11")
    ]),
    TestCase("Check Working", [
        ("IN", "7+5*(2-3)/2;"),
        ("OUT", "=4.5", "=4.5")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120'))
]
