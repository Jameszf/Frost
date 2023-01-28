
from frost import bitboard
import unittest


class TestBitboardFunctions(unittest.TestCase):
    def test_fbitscran_selected_cases(self):
        with open("tests/fbitscanTests.txt") as f:
            for line in f:
                num, ans = [x.strip() for x in line.split(", ")]
                output = bitboard.fBitscan(int(num, 16))
                self.assertEqual(output, int(ans), f"Incorrect output for {num}. Expected: {ans} | Actual: {output}")

    def test_fbitscan_random_cases(self):
        with open("tests/fbitscanTests.random.txt") as f:
            for line in f:
                num, ans = [x.strip() for x in line.split(", ")]
                output = bitboard.fBitscan(int(num, 16))
                self.assertEqual(output, int(ans), f"Incorrect output for {num}. Expected: {ans} | Actual: {output}")


if __name__ == "__main__":
    unittest.main()
