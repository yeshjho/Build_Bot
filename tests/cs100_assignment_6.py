from test_case import TestCase
from error_test import ErrorTest

is_unittest = False

tests = [
    TestCase("(1)IsEven - Odd", [
        ("IN", "1"),
        ("IN", "FFF"),
        ("OUT", "0xfff is odd", "0xfff is odd")
    ]),
    TestCase("(1)IsEven - Even", [
        ("IN", "1"),
        ("IN", "F8"),
        ("OUT", "0xf8 is even", "0xf8 is even")
    ]),
    TestCase("(2)IsNegative - Positive", [
        ("IN", "2"),
        ("IN", "C879"),
        ("OUT", "0xc879 is positive", "0xc879 is positive")
    ]),
    TestCase("(2)IsNegative - Negative", [
        ("IN", "2"),
        ("IN", "8FFCA563"),
        ("OUT", "0x8ffca563 is negative", "0x8ffca563 is negative")
    ]),
    TestCase("(3)IsBitSet - Normal", [
        ("IN", "3"),
        ("IN", "1234"),
        ("IN", "4"),
        ("OUT", "Bit 4 of 0x1234 is set", "Bit 4 of 0x1234 is set")
    ]),
    TestCase("(3)IsBitSet - 0th", [
        ("IN", "3"),
        ("IN", "1234"),
        ("IN", "0"),
        ("OUT", "Bit 0 of 0x1234 is not set", "Bit 0 of 0x1234 is not set")
    ]),
    TestCase("(4)BitCount_BruteForce", [
        ("IN", "4"),
        ("IN", "12345678"),
        ("OUT", "0x12345678 has 13 bits set", "0x12345678 has 13 bits set")
    ]),
    TestCase("(5)SetBit - Normal", [
        ("IN", "5"),
        ("IN", "F780"),
        ("IN", "6"),
        ("OUT", "If you set bit 6 of 0xf780 it becomes 0xf7c0", "If you set bit 6 of 0xf780 it becomes 0xf7c0")
    ]),
    TestCase("(5)SetBit - Setting 1 to 1", [
        ("IN", "5"),
        ("IN", "F780"),
        ("IN", "7"),
        ("OUT", "If you set bit 7 of 0xf780 it becomes 0xf780", "If you set bit 7 of 0xf780 it becomes 0xf780")
    ]),
    TestCase("(5)SetBit - 0th", [
        ("IN", "5"),
        ("IN", "12345678"),
        ("IN", "0"),
        ("OUT", "If you set bit 0 of 0x12345678 it becomes 0x12345679",
         "If you set bit 0 of 0x12345678 it becomes 0x12345679")
    ]),
    TestCase("(6)ClearBit - Normal", [
        ("IN", "6"),
        ("IN", "76A2"),
        ("IN", "5"),
        ("OUT", "Bit 5 cleared from 0x76a2 is 0x7682", "Bit 5 cleared from 0x76a2 is 0x7682")
    ]),
    TestCase("(6)ClearBit - Clearing 0", [
        ("IN", "6"),
        ("IN", "EEE2"),
        ("IN", "4"),
        ("OUT", "Bit 4 cleared from 0xeee2 is 0xeee2", "Bit 4 cleared from 0xeee2 is 0xeee2")
    ]),
    TestCase("(6)ClearBit - 0th", [
        ("IN", "6"),
        ("IN", "ABCD"),
        ("IN", "0"),
        ("OUT", "Bit 0 cleared from 0xabcd is 0xabcc", "Bit 0 cleared from 0xabcd is 0xabcc")
    ]),
    TestCase("(7)ClearBitRange - Normal", [
        ("IN", "7"),
        ("IN", "ABCDEF"),
        ("IN", "2"),
        ("IN", "10"),
        ("OUT", "Clear bits 2 to 10 from 0xabcdef is 0xabc803", "Clear bits 2 to 10 from 0xabcdef is 0xabc803")
    ]),
    TestCase("(7)ClearBitRange - One Bit", [
        ("IN", "7"),
        ("IN", "ABCDEF"),
        ("IN", "5"),
        ("IN", "5"),
        ("OUT", "Clear bits 5 to 5 from 0xabcdef is 0xabcdcf", "Clear bits 5 to 5 from 0xabcdef is 0xabcdcf")
    ]),
    TestCase("(7)ClearBitRange - 0 to 0", [
        ("IN", "7"),
        ("IN", "ABCDEF"),
        ("IN", "0"),
        ("IN", "0"),
        ("OUT", "Clear bits 0 to 0 from 0xabcdef is 0xabcdee", "Clear bits 0 to 0 from 0xabcdef is 0xabcdee")
    ]),
    TestCase("(8)EvenOddBitSwap - 1", [
        ("IN", "8"),
        ("IN", "AAAAAAAA"),
        ("OUT", "0xaaaaaaaa when swapped even/odd bits becomes 0x55555555",
         "0xaaaaaaaa when swapped even/odd bits becomes 0x55555555")
    ]),
    TestCase("(8)EvenOddBitSwap - 2", [
        ("IN", "8"),
        ("IN", "12345678"),
        ("OUT", "0x12345678 when swapped even/odd bits becomes 0x2138a9b4",
         "0x12345678 when swapped even/odd bits becomes 0x2138a9b4")
    ]),
    TestCase("(9)BitSwap - 0 and 0", [
        ("IN", "9"),
        ("IN", "E82"),
        ("IN", "2"),
        ("IN", "5"),
        ("OUT", "Swap bit 2 with bit 5 in 0xe82 is 0xe82", "Swap bit 2 with bit 5 in 0xe82 is 0xe82")
    ]),
    TestCase("(9)BitSwap - 0 and 1", [
        ("IN", "9"),
        ("IN", "E82"),
        ("IN", "2"),
        ("IN", "9"),
        ("OUT", "Swap bit 2 with bit 9 in 0xe82 is 0xc86", "Swap bit 2 with bit 9 in 0xe82 is 0xc86")
    ]),
    TestCase("(9)BitSwap - 1 and 1", [
        ("IN", "9"),
        ("IN", "E82"),
        ("IN", "9"),
        ("IN", "1"),
        ("OUT", "Swap bit 9 with bit 1 in 0xe82 is 0xe82", "Swap bit 9 with bit 1 in 0xe82 is 0xe82")
    ]),
    TestCase("(9)BitSwap - 0th", [
        ("IN", "9"),
        ("IN", "8F"),
        ("IN", "6"),
        ("IN", "0"),
        ("OUT", "Swap bit 6 with bit 0 in 0x8f is 0xce", "Swap bit 6 with bit 0 in 0x8f is 0xce")
    ]),
    TestCase("(9)BitSwap - Self", [
        ("IN", "9"),
        ("IN", "159BD"),
        ("IN", "4"),
        ("IN", "4"),
        ("OUT", "Swap bit 4 with bit 4 in 0x159bd is 0x159bd", "Swap bit 4 with bit 4 in 0x159bd is 0x159bd")
    ]),
    TestCase("(10)XORSwap", [
        ("IN", "10"),
        ("IN", "87DF2A3"),
        ("IN", "109C3EE"),
        ("OUT", "Swap 0x87df2a3 and 0x109c3ee becomes 0x109c3ee and 0x87df2a3",
         "Swap 0x87df2a3 and 0x109c3ee becomes 0x109c3ee and 0x87df2a3")
    ]),
    TestCase("(11)BitCount_Fast", [
        ("IN", "11"),
        ("IN", "12345678"),
        ("OUT", "0x12345678 has 13 bits set", "0x12345678 has 13 bits set")
    ])
]

error_tests = [
    ErrorTest("Header Comment", "Your header comment is incorrect or missing",
              ErrorTest.check_header_comment('copyright(c)')),
    ErrorTest("Usage of + or - or * or /",
              "Your code includes + or - or * or /. It might be okay, just telling you it exists",
              ErrorTest.get_function_contains(r"[^\+]\+[^\+]", should_contain=False))
]
