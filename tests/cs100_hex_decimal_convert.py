from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase('Dec to Hex - Normal', [
        ("IN", "1"),
        ("IN", "1025"),
        ("OUT", r"Hex String = 0x401\b", "Hex String = 0x401")
    ]),
    TestCase('Dec to Hex - Zero', [
        ("IN", "1"),
        ("IN", "0"),
        ("OUT", r"Hex String = 0x0\b", "Hex String = 0x0")
    ]),
    TestCase("Hex to Dec - Alphabet", [
        ("IN", "2"),
        ("IN", "ABCDEF"),
        ("OUT", r"Decimal = 11259375\b", "Decimal = 11259375")
    ]),
    TestCase("Hex to Dec - Number", [
        ("IN", "2"),
        ("IN", "12035"),
        ("OUT", r"Decimal = 73781\b", "Decimal = 73781")
    ]),
    TestCase("Hex to Dec - Alphanumeric", [
        ("IN", "2"),
        ("IN", "A5F87"),
        ("OUT", r"Decimal = 679815\b", "Decimal = 679815")
    ]),
    TestCase("Hex to Dec - Zero", [
        ("IN", "2"),
        ("IN", "0"),
        ("OUT", r"Decimal = 0\b", "Decimal = 0")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs100'))
]
