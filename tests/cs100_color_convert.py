from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase("Valid Input - 24 to RGB", [
        ("IN", "1"),
        ("IN", "F58E22"),
        ("OUT", "RGB = \(245, 142, 34\)", "RGB = (245, 142, 34)")
    ]),
    TestCase("Valid Input - GBA to RGB", [
        ("IN", "2"),
        ("IN", "78AF"),
        ("OUT", "RGB = \(120, 40, 240\)", "RGB = (120, 40, 240)")
    ]),
    TestCase("Valid Input - RGB to GBA, Lossy", [
        ("IN", "3"),
        ("IN", "02F48B"),
        ("OUT", "GBA Color = 0x47c0", "GBA Color = 0x47c0")
    ]),
    TestCase("Valid Input - RGB to GBA, Not Lossy", [
        ("IN", "3"),
        ("IN", "F88068"),
        ("OUT", "GBA Color = 0x361f", "GBA Color = 0x361f")
    ]),
    TestCase("Invalid Input - 24 Bits", [
        ("IN", "1"),
        ("IN", "1FFFFFF"),
        ("OUT", "24 Bit Color is not valid", "24 Bit Color is not valid")
    ]),
    TestCase("Invalid Input - 16 Bits", [
        ("IN", "2"),
        ("IN", "8FFF"),
        ("OUT", "16 Bit Color is not valid", "16 Bit Color is not valid")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('copyright(c)'))
]
