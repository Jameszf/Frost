
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

    def test_ms1b(self):
        cases = [
            (0b0001_0000, 0b0001_0000),
            (0b0101_1010, 0b0100_0000),
            (0b0000_0101, 0b0000_0100),
            (0x0000_F000, 0x0000_8000)
        ]
        for case in cases:
            num, ans = case
            output = bitboard.ms1b(num)
            self.assertEqual(output, ans, f"Incorrect output for {num}. Expected: {ans} | Actual: {output}")

    def test_ls1b(self):
        cases = [
            (0b0001_0000, 0b0001_0000),
            (0b0101_1010, 0b0000_0010),
            (0b0000_0101, 0b0000_0001),
            (0x0000_F000, 0x0000_1000)
        ]
        for case in cases:
            num, ans = case
            output = bitboard.ls1b(num)
            self.assertEqual(output, ans, f"Incorrect output for {num}. Expected: {ans} | Actual: {output}")

    def test_getBit(self):
        bStr = "00010101110001011000"
        for i in range(len(bStr)):
            ans = int(bStr[len(bStr) - i - 1])
            output = bitboard.getBit(int(bStr, 2), i)
            self.assertEqual(output, ans, f"Incorrect output at index {i}. Expected: {ans} | Actual: {output}")

    def test_clearBit(self):
        cases = [
            (0b1000_0000, 7, 0b0000_0000),
            (0b1001_0000, 0, 0b1001_0000),
            (0b1111_1111, 10, 0b1111_1111),
            (0xFFFF_FFFF, 18, 0xFFFB_FFFF)
        ]
        for case in cases:
            num, idx, ans = case
            output = bitboard.clearBit(num, idx)
            self.assertEqual(output, ans, f"Incorrect output for {num} at index {idx}. Expected: {ans} | Actual: {output}")

    def test_setBit(self):
        cases = [
            (0b1000_0000, 7, 0b1000_0000),
            (0b1001_0000, 0, 0b1001_0001),
            (0b1111_1111, 10, 0b0100_1111_1111),
            (0xFFFF_FFFF, 18, 0xFFFF_FFFF)
        ]
        for case in cases:
            num, idx, ans = case
            output = bitboard.setBit(num, idx)
            self.assertEqual(output, ans, f"Incorrect output for {num} at index {idx}. Expected: {ans} | Actual: {output}")

    def test_flipBit(self):
        cases = [
            (0b1000_0000, 7, 0b0000_0000),
            (0b1001_0000, 0, 0b1001_0001),
            (0b1111_1111, 10, 0b0100_1111_1111),
            (0xFFFF_FFFF, 18, 0xFFFB_FFFF),
        ]
        for case in cases:
            num, idx, ans = case
            output = bitboard.flipBit(num, idx)
            self.assertEqual(output, ans, f"Incorrect output for {num} at index {idx}. Expected: {ans} | Actual: {output}")

        

if __name__ == "__main__":
    unittest.main()
