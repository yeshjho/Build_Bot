from test_case import TestCase
from error_test import ErrorTest

tests = [
    TestCase("Normal", [
        ("OUT", r"[^1]*2\s+3\s+5\s+7\s+11\s+13\s+17\s+19\s+23\s+29\s+31\s+37"
                r"\s+41\s+43\s+47\s+53\s+59\s+61\s+67\s+71\s+73\s+79\s+83\s+89\s+97[^(101)]*",
         "2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97 (Space, \\n, \\t... doesn't matter)")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing", ErrorTest.check_header_comment('cs120')),
    ErrorTest("Missing IsPrimNumber", "The exercise suggest you make a function, IsPrimeNumber, but there isn't",
              ErrorTest.get_function_contains(r'bool\s+IsPrimeNumber\(int\s+\w+\)'))
]
