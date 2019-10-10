from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase("Subtract - Normal", [
        ("IN", "1"),
        ("IN", "53"),
        ("IN", "20"),
        ("OUT", TestCase.get_regex_contains("Difference is:  33"), "Difference is:  33")
    ]),
    TestCase("Subtract - Big Number", [
        ("IN", "1"),
        ("IN", "789546123"),
        ("IN", "4587853"),
        ("OUT", TestCase.get_regex_contains("Difference is:  784958270"), "Difference is:  784958270")
    ]),
    TestCase("Subtract - Negative Result", [
        ("IN", "1"),
        ("IN", "45620"),
        ("IN", "8791233"),
        ("OUT", TestCase.get_regex_contains("Difference is:  -8745613"), "Difference is:  -8745613")
    ]),
    TestCase("Subtract - 0", [
        ("IN", "1"),
        ("IN", "0"),
        ("IN", "0"),
        ("OUT", TestCase.get_regex_contains("Difference is:  0"), "Difference is:  0")
    ]),
    TestCase("Division - No Remainder", [
        ("IN", "2"),
        ("IN", "1482"),
        ("IN", "57"),
        ("OUT", TestCase.get_regex_contains(r"Result \(the Quotient\) is:  26"), "Result (the Quotient) is:  26")
    ]),
    TestCase("Division - with Remainder", [
        ("IN", "2"),
        ("IN", "785"),
        ("IN", "9"),
        ("OUT", TestCase.get_regex_contains(r"Result \(the Quotient\) is:  87"), "Result (the Quotient) is:  87")
    ]),
    TestCase("Division - Big Number", [
        ("IN", "2"),
        ("IN", "15246879"),
        ("IN", "15478"),
        ("OUT", TestCase.get_regex_contains(r"Result \(the Quotient\) is:  985"), "Result (the Quotient) is:  985")
    ]),
    TestCase("Division - Dividing 0", [
        ("IN", "2"),
        ("IN", "0"),
        ("IN", "7865"),
        ("OUT", TestCase.get_regex_contains(r"Result \(the Quotient\) is:  0"), "Result (the Quotient) is:  0")
    ]),
    TestCase("Division - 0, reversed input", [
        ("IN", "2"),
        ("IN", "56"),
        ("IN", "0"),
        ("OUT", "EXCEPTION", "(An exception should be thrown)")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('copyright(c)')),
    ErrorTest("Usage of + or - or * or /", "Your code includes + or - or * or /",
              ErrorTest.get_function_contains(r"\+", should_contain=False))
]
