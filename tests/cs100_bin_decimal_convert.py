from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase('Dec to Bin - Normal', [
        ("IN", "1"),
        ("IN", "348"),
        ("OUT", r"Binary String = 0b101011100\b", "Binary String = 0b101011100")
    ]),
    TestCase('Dec to Bin - Zero', [
        ("IN", "1"),
        ("IN", "0"),
        ("OUT", r"Binary String = 0b0\b", "Binary String = 0b0")
    ]),
    TestCase("Bin to Dec - Normal", [
        ("IN", "2"),
        ("IN", "110101110"),
        ("OUT", r"Decimal = 430\b", "Decimal = 430")
    ]),
    TestCase("Bin to Dec - Zero", [
        ("IN", "2"),
        ("IN", "0"),
        ("OUT", r"Decimal = 0\b", "Decimal = 0")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs100'))
]
