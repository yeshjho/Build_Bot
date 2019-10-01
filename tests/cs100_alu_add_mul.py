from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase("Addition - Normal", [
        ("IN", "1"),
        ("IN", "20"),
        ("IN", "10"),
        ("OUT", r"\bSum is:  30\b", "Sum is:  30")
    ]),
    TestCase("Addition - Big Number", [
        ("IN", "1"),
        ("IN", "4587853"),
        ("IN", "789546123"),
        ("OUT", r"\bSum is:  794133976\b", "Sum is:  794133976")
    ]),
    TestCase("Addition - 0", [
        ("IN", "1"),
        ("IN", "0"),
        ("IN", "0"),
        ("OUT", r"\bSum is:  0\b", "Sum is:  0")
    ]),
    TestCase("Multiplication - Normal", [
        ("IN", "2"),
        ("IN", "21"),
        ("IN", "57"),
        ("OUT", r"\bProduct is:  1197\b", "Product is:  1197")
    ]),
    TestCase("Multiplication - Big Number", [
        ("IN", "2"),
        ("IN", "4587"),
        ("IN", "7893"),
        ("OUT", r"\bProduct is:  36205191\b", "Product is:  36205191")
    ]),
    TestCase("Multiplication - 0", [
        ("IN", "2"),
        ("IN", "43"),
        ("IN", "0"),
        ("OUT", r"\bProduct is:  0\b", "Product is:  0")
    ]),
    TestCase("Multiplication - 0, reversed input", [
        ("IN", "2"),
        ("IN", "0"),
        ("IN", "434"),
        ("OUT", r"\bProduct is:  0\b", "Product is:  0")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs100')),
    ErrorTest("Usage of + or - or *", "Your code includes + or - or *",
              ErrorTest.get_function_contains(r"\+", should_contain=False))
]
