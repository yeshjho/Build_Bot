from test_case import TestCase
from error_test import ErrorTest

is_unittest = False

tests = []

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120')),
]
