
from frost import bitboard
import unittest


class TestBitboardFunctions(unittest.TestCase):
    def test_fbitscran_basic(self):
        cases = [
            (0b0000_0001, 0),
            (0b1111_0000, 4),
            (0b1010_0101, 0),
            (0b0010_0000, 5),
            (0b1000_0000, 7),
            (0x8000000000000000000000000, 99),
            (0xFFFFFFFFFFFFFFFFFFFFFFFF1, 0),
            (0x9000000000000000000000000, 96),
            (0x8100000000000000000000000, 92),
        ]
        for case in cases:
            num, ans = case
            output = bitboard.fBitscan(num)
            self.assertEqual(output, ans, f"Incorrect output for {num}. Expected: {ans} | Actual: {output}")


    def test_rbitscan_basic(self):
        cases = [
            (0b0000_0001, 0),
            (0b1111_0000, 7),
            (0b0000_0101, 2),
            (0b0010_0000, 5),
            (0b1000_0000, 7),
            (0x8000000000000000000000000, 99),
            (0x80000000000000000000000, 91),
            (0x8FFFFFFFFFFFFFFFFFFFFFFFF, 99),
            (0x0008FFFFFFFFFFFFFFFFFFFFF, 87),
        ]
        for case in cases:
            num, ans = case
            output = bitboard.rBitscan(num)
            self.assertEqual(output, ans, f"Incorrect output for {num}. Expected: {ans} | Actual: {output}")
            

if __name__ == "__main__":
    unittest.main()
